import { afterEach, describe, expect, it } from 'vitest';
import { PreferenceEngine, attributeName, OVERLAY_HOST_ID } from '../../src/managers/PreferenceEngine';
import {
  TEXT_SCALE_STYLE_ID,
  buildTextScaleCss,
  isScalableFontSize,
  scopeSelector,
  splitSelectors,
} from '../../src/managers/TypographyManager';
import { GUIDE_ID, MASK_BOTTOM_ID, MASK_TOP_ID } from '../../src/managers/ReadingToolsManager';
import { PREFERENCE_KEYS, defaultPreferences } from '../../src/preferences';
import type { AccessibilityPreferences } from '../../src/types';

const options = {
  zIndex: 95,
  readingGuide: { color: '#0B7FB3', thickness: 4, followFocus: true },
  readingMask: { opacity: 0.5, areaHeight: 120, followFocus: true },
};

const everything: AccessibilityPreferences = {
  textScale: 1.3, readableFont: true, letterSpacing: 0.1, wordSpacing: 0.2, lineHeight: 1.75,
  pauseAnimations: true, reduceMotion: true, grayscale: true, highContrast: true, darkContrast: false,
  lightContrast: false, invertColors: false, highlightLinks: true, highlightHeadings: true, readingGuide: true,
  readingMask: true, largeCursor: true, focusHighlight: true, hideImages: true,
};

const root = (): HTMLElement => document.documentElement;

afterEach(() => {
  document.head.innerHTML = '';
  document.body.innerHTML = '';
  for (const attr of Array.from(root().attributes)) if (attr.name.startsWith('data-a11y-toolbar')) root().removeAttribute(attr.name);
  root().removeAttribute('style');
});

describe('attributeName', () => {
  it('maps each preference to a namespaced kebab-case attribute', () => {
    expect(attributeName('textScale')).toBe('data-a11y-toolbar-text-scale');
    expect(attributeName('highlightLinks')).toBe('data-a11y-toolbar-highlight-links');
    expect(attributeName('hideImages')).toBe('data-a11y-toolbar-hide-images');
  });
});

describe('PreferenceEngine', () => {
  it('adds an attribute only for active preferences', () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply(everything);
    for (const key of PREFERENCE_KEYS) {
      const active = key !== 'darkContrast' && key !== 'lightContrast' && key !== 'invertColors';
      expect(root().hasAttribute(attributeName(key)), key).toBe(active);
    }
    expect(root().getAttribute('data-a11y-toolbar-text-scale')).toBe('1.3');
    expect(root().getAttribute('data-a11y-toolbar-line-height')).toBe('1.75');
  });

  it('sets and removes the preference CSS variables', () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply(everything);
    expect(root().style.getPropertyValue('--a11y-toolbar-text-scale')).toBe('1.3');
    expect(root().style.getPropertyValue('--a11y-toolbar-letter-spacing')).toBe('0.1em');
    expect(root().style.getPropertyValue('--a11y-toolbar-word-spacing')).toBe('0.2em');
    expect(root().style.getPropertyValue('--a11y-toolbar-line-height')).toBe('1.75');
    engine.apply(defaultPreferences);
    expect(root().getAttribute('style')).toBeNull();
  });

  it('does not touch unrelated attributes, classes or inline styles on <html>', () => {
    root().className = 'host-class';
    root().setAttribute('data-theme', 'dark');
    root().style.setProperty('--host-var', '1');
    const engine = new PreferenceEngine(document, options);
    engine.apply(everything);
    engine.clear();
    expect(root().className).toBe('host-class');
    expect(root().getAttribute('data-theme')).toBe('dark');
    expect(root().style.getPropertyValue('--host-var')).toBe('1');
    root().className = '';
    root().removeAttribute('data-theme');
  });

  it('creates the reading guide and both mask overlays, hidden from assistive technology and pointer events', () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply({ ...defaultPreferences, readingGuide: true, readingMask: true });
    const host = document.getElementById(OVERLAY_HOST_ID);
    expect(host?.getAttribute('aria-hidden')).toBe('true');
    for (const id of [GUIDE_ID, MASK_TOP_ID, MASK_BOTTOM_ID]) {
      const el = document.getElementById(id);
      expect(el, id).not.toBeNull();
      expect(el?.getAttribute('aria-hidden')).toBe('true');
      expect(el?.hasAttribute('tabindex')).toBe(false);
    }
    engine.apply({ ...defaultPreferences, readingMask: true });
    expect(document.getElementById(GUIDE_ID)).toBeNull();
    expect(document.getElementById(MASK_TOP_ID)).not.toBeNull();
    engine.apply(defaultPreferences);
    expect(document.getElementById(OVERLAY_HOST_ID)).toBeNull();
    expect(document.getElementById(MASK_BOTTOM_ID)).toBeNull();
  });

  it('moves the reading guide with the pointer', async () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply({ ...defaultPreferences, readingGuide: true });
    window.dispatchEvent(new MouseEvent('pointermove', { clientY: 200 }));
    await new Promise((resolve) => requestAnimationFrame(resolve));
    expect(document.getElementById(GUIDE_ID)?.style.transform).toBe('translate3d(0, 198px, 0)');
    engine.clear();
  });

  it('keeps the focused element inside the clear band of the mask', async () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply({ ...defaultPreferences, readingMask: true });
    const input = document.createElement('input');
    document.body.appendChild(input);
    input.getBoundingClientRect = () => ({ top: 300, height: 300, bottom: 600, left: 0, right: 10, width: 10, x: 0, y: 300, toJSON: () => ({}) });
    input.focus();
    await new Promise((resolve) => requestAnimationFrame(resolve));
    const top = Number.parseFloat(document.getElementById(MASK_TOP_ID)?.style.height ?? '0');
    const bottom = Number.parseFloat(document.getElementById(MASK_BOTTOM_ID)?.style.top ?? '0');
    expect(top).toBeLessThanOrEqual(300);
    expect(bottom).toBeGreaterThanOrEqual(Math.min(600, window.innerHeight));
    engine.clear();
  });

  it('generates the text-scale sheet only while text is scaled', () => {
    const style = document.createElement('style');
    style.textContent = 'p { font-size: 16px } .big, h1::before { font-size: 2rem } @media (min-width: 1px) { .x { font-size: 20px } }';
    document.head.appendChild(style);
    const engine = new PreferenceEngine(document, options);
    engine.apply({ ...defaultPreferences, textScale: 1.2 });
    const generated = document.getElementById(TEXT_SCALE_STYLE_ID);
    expect(generated?.textContent).toContain('font-size:calc(16px * var(--a11y-toolbar-text-scale)) !important');
    expect(generated?.textContent).toContain('@media');
    expect(generated?.textContent).not.toContain('2rem');
    engine.apply(defaultPreferences);
    expect(document.getElementById(TEXT_SCALE_STYLE_ID)).toBeNull();
  });

  it('clear() removes every attribute, variable, sheet and overlay', () => {
    const engine = new PreferenceEngine(document, options);
    engine.apply(everything);
    engine.clear();
    expect(Array.from(root().attributes).some((a) => a.name.startsWith('data-a11y-toolbar'))).toBe(false);
    expect(root().getAttribute('style')).toBeNull();
    expect(document.querySelector('[id^="a11y-toolbar"]')).toBeNull();
  });
});

describe('text scale helpers', () => {
  it('splits selector lists on top-level commas only', () => {
    expect(splitSelectors('a, b:is(c, d), [data-x="1,2"]')).toEqual(['a', 'b:is(c, d)', '[data-x="1,2"]']);
  });

  it('adds the exclusion before pseudo-elements', () => {
    expect(scopeSelector('p')).toMatch(/^p:not\(/);
    expect(scopeSelector('h1::before')).toMatch(/^h1:not\(.*\)::before$/);
  });

  it('scales only absolute and viewport sizes', () => {
    expect(isScalableFontSize('14px')).toBe(true);
    expect(isScalableFontSize('clamp(20px, 4vw, 40px)')).toBe(true);
    expect(isScalableFontSize('1.2rem')).toBe(false);
    expect(isScalableFontSize('1.2em')).toBe(false);
    expect(isScalableFontSize('120%')).toBe(false);
    expect(isScalableFontSize('inherit')).toBe(false);
  });

  it('skips the toolbar own stylesheets', () => {
    const own = document.createElement('style');
    own.id = 'a11y-toolbar-runtime-styles';
    own.textContent = '.a11y-toolbar-root { font-size: 15px }';
    document.head.appendChild(own);
    expect(buildTextScaleCss(document)).not.toContain('15px');
  });
});
