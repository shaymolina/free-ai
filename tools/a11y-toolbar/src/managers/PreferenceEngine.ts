import type {
  AccessibilityPreferences,
  PreferenceKey,
  ResolvedReadingGuideOptions,
  ResolvedReadingMaskOptions,
} from '../types';
import { PREFERENCE_KEYS } from '../preferences';
import { ReadingGuideManager, ReadingMaskManager } from './ReadingToolsManager';
import { SCALE_VAR, TypographyManager } from './TypographyManager';
import { bodyOf } from '../utils/browser';

export const ATTRIBUTE_PREFIX = 'data-a11y-toolbar-';
export const GRAYSCALE_LAYER_ID = 'a11y-toolbar-grayscale-layer';
export const BACKDROP_ATTR = 'data-a11y-toolbar-backdrop';
export const OVERLAY_HOST_ID = 'a11y-toolbar-overlays';

/** camelCase preference key to its kebab-case root attribute. */
export function attributeName(key: PreferenceKey): string {
  return ATTRIBUTE_PREFIX + key.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`);
}

const CSS_VARS: Partial<Record<PreferenceKey, string>> = {
  textScale: SCALE_VAR,
  letterSpacing: '--a11y-toolbar-letter-spacing',
  wordSpacing: '--a11y-toolbar-word-spacing',
  lineHeight: '--a11y-toolbar-line-height',
};

function cssValue(key: PreferenceKey, value: number): string {
  return key === 'letterSpacing' || key === 'wordSpacing' ? `${value}em` : String(value);
}

function isActive(value: boolean | number, key: PreferenceKey): boolean {
  if (typeof value === 'boolean') return value;
  return key === 'textScale' ? value !== 1 : value !== 0;
}

function supportsBackdrop(win: Window | null): boolean {
  const css: { supports?: (property: string, value: string) => boolean } | undefined = win ? (win as Window & { CSS?: typeof CSS }).CSS : undefined;
  if (!css || typeof css.supports !== 'function') return false;
  return css.supports('backdrop-filter', 'grayscale(1)') || css.supports('-webkit-backdrop-filter', 'grayscale(1)');
}

export interface EngineOptions {
  readonly zIndex: number;
  readonly readingGuide: ResolvedReadingGuideOptions;
  readonly readingMask: ResolvedReadingMaskOptions;
}

/**
 * Turns the preference object into reversible page changes: namespaced attributes and variables
 * on <html>, one generated text-scale sheet and a few overlay elements. Host markup is never edited.
 */
export class PreferenceEngine {
  private readonly root: HTMLElement;
  private readonly typography: TypographyManager;
  private readonly backdrop: boolean;
  private guide: ReadingGuideManager | null = null;
  private mask: ReadingMaskManager | null = null;
  private overlayHost: HTMLDivElement | null = null;
  private grayscaleLayer: HTMLDivElement | null = null;
  private pending: AccessibilityPreferences | null = null;
  private readonly onReady = (): void => {
    const prefs = this.pending;
    this.pending = null;
    if (prefs) this.apply(prefs);
  };

  constructor(private readonly doc: Document, private readonly options: EngineOptions) {
    this.root = doc.documentElement;
    this.typography = new TypographyManager(doc);
    this.backdrop = supportsBackdrop(doc.defaultView);
  }

  /** Overlays live in one fixed, non-interactive container next to the toolbar. */
  private host(): HTMLDivElement | null {
    if (this.overlayHost?.isConnected) return this.overlayHost;
    const body = bodyOf(this.doc);
    if (!body) return null;
    const host = this.doc.createElement('div');
    host.id = OVERLAY_HOST_ID;
    host.setAttribute('aria-hidden', 'true');
    host.setAttribute('data-a11y-toolbar-overlay', '');
    host.style.zIndex = String(Math.max(0, this.options.zIndex - 1));
    body.appendChild(host);
    this.overlayHost = host;
    this.guide = new ReadingGuideManager(this.doc, host, this.options.readingGuide);
    this.mask = new ReadingMaskManager(this.doc, host, this.options.readingMask);
    return host;
  }

  private dropHost(): void {
    this.guide?.destroy();
    this.mask?.destroy();
    this.guide = null;
    this.mask = null;
    this.overlayHost?.remove();
    this.overlayHost = null;
  }

  apply(prefs: AccessibilityPreferences): void {
    for (const key of PREFERENCE_KEYS) {
      try {
        this.applyKey(key, prefs[key]);
      } catch {
        /* One failing preference must not stop the rest. */
      }
    }
    this.safely(() => this.typography.update(prefs.textScale));
    if (!bodyOf(this.doc)) {
      // Attributes are already on <html>; elements wait for <body>.
      if (!this.pending) this.doc.addEventListener('DOMContentLoaded', this.onReady, { once: true });
      this.pending = prefs;
      return;
    }
    this.safely(() => this.updateGrayscale(prefs.grayscale));
    this.safely(() => {
      if (prefs.readingGuide || prefs.readingMask) {
        this.host();
        this.guide?.update(prefs.readingGuide);
        this.mask?.update(prefs.readingMask);
      } else {
        this.dropHost();
      }
    });
  }

  /** Re-reads host stylesheets for text scaling. */
  refreshTextScale(): void {
    this.safely(() => this.typography.refresh());
  }

  /** Removes every attribute, variable and element this engine created. */
  clear(): void {
    for (const key of PREFERENCE_KEYS) {
      this.root.removeAttribute(attributeName(key));
      const cssVar = CSS_VARS[key];
      if (cssVar) this.root.style.removeProperty(cssVar);
    }
    this.root.removeAttribute(BACKDROP_ATTR);
    if (this.root.getAttribute('style') === '') this.root.removeAttribute('style');
    this.typography.remove();
    this.updateGrayscale(false);
    this.dropHost();
    this.doc.removeEventListener('DOMContentLoaded', this.onReady);
    this.pending = null;
  }

  private applyKey(key: PreferenceKey, value: boolean | number): void {
    const attr = attributeName(key);
    const cssVar = CSS_VARS[key];
    if (isActive(value, key)) {
      this.root.setAttribute(attr, typeof value === 'boolean' ? '' : String(value));
      if (cssVar && typeof value === 'number') this.root.style.setProperty(cssVar, cssValue(key, value));
    } else {
      this.root.removeAttribute(attr);
      if (cssVar) this.root.style.removeProperty(cssVar);
    }
    if (this.root.getAttribute('style') === '') this.root.removeAttribute('style');
  }

  private updateGrayscale(active: boolean): void {
    if (!active || !this.backdrop) {
      this.grayscaleLayer?.remove();
      this.grayscaleLayer = null;
      this.root.removeAttribute(BACKDROP_ATTR);
      return;
    }
    this.root.setAttribute(BACKDROP_ATTR, '');
    if (this.grayscaleLayer) return;
    const layer = this.doc.createElement('div');
    layer.id = GRAYSCALE_LAYER_ID;
    layer.setAttribute('aria-hidden', 'true');
    layer.setAttribute('data-a11y-toolbar-overlay', '');
    layer.style.zIndex = String(Math.max(0, this.options.zIndex - 1));
    (bodyOf(this.doc) ?? this.root).appendChild(layer);
    this.grayscaleLayer = layer;
  }

  private safely(fn: () => void): void {
    try {
      fn();
    } catch {
      /* Keep the host page and the toolbar working. */
    }
  }
}
