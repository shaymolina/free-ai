import { PREFERENCE_KEYS, PreferencesManager, defaultPreferences, isDefault } from './preferences';
import type {
  AccessibilityPreferences,
  AccessibilityProviderProps,
  BooleanPreferenceKey,
  ContrastMode,
  PreferenceKey,
  PreferencesListenerArgs,
  ResolvedReadingGuideOptions,
  ResolvedReadingMaskOptions,
  SteppedPreferenceKey,
  Unsubscribe,
} from './types';
import { DEFAULT_STORAGE_KEY, StorageManager, SyncManager } from './managers/StorageManager';
import { PreferenceEngine } from './managers/PreferenceEngine';
import { acquireRuntimeStyles, runtimeStyleRefs } from './managers/StyleManager';
import { clampNumber, getDocument, getWindow, isSafeColor } from './utils/browser';
import toolbarCss from './styles/accessibility-toolbar.css?raw';
import preferencesCss from './styles/accessibility-preferences.css?raw';

export const RUNTIME_CSS = `${preferencesCss}\n${toolbarCss}`;
export const PREFERENCE_EVENT = 'a11y-toolbar:preferences-change';
export const DEFAULT_Z_INDEX = 95;

export function resolveGuideOptions(input: AccessibilityProviderProps['readingGuideOptions']): ResolvedReadingGuideOptions {
  return {
    color: isSafeColor(input?.color) ? input.color : '#0B7FB3',
    thickness: clampNumber(input?.thickness, 2, 16, 4),
    followFocus: input?.followFocus ?? true,
  };
}

export function resolveMaskOptions(input: AccessibilityProviderProps['readingMaskOptions']): ResolvedReadingMaskOptions {
  return {
    opacity: clampNumber(input?.opacity, 0.2, 0.85, 0.55),
    areaHeight: clampNumber(input?.areaHeight, 40, 400, 120),
    followFocus: input?.followFocus ?? true,
  };
}

export function sanitizeStorageKey(key: unknown): string {
  return typeof key === 'string' && /^[\w:.-]{1,100}$/.test(key) ? key : DEFAULT_STORAGE_KEY;
}

export interface ProviderInternalOptions {
  readonly zIndex?: number;
}

/**
 * Owns the preference state, persistence, cross-tab sync and the page engine.
 * Safe to construct on the server: without a document it keeps state in memory and touches nothing.
 */
export class AccessibilityProvider {
  private readonly manager: PreferencesManager;
  private readonly storage: StorageManager;
  private readonly sync: SyncManager;
  private readonly engine: PreferenceEngine | null;
  private readonly doc: Document | null;
  private releaseStyles: () => void = () => undefined;
  private unsubscribe: Unsubscribe = () => undefined;
  private remoteUpdate = false;
  private destroyed = false;

  constructor(props: AccessibilityProviderProps = {}, internal: ProviderInternalOptions = {}) {
    this.doc = getDocument(props.document);
    const win = getWindow(this.doc);
    this.storage = new StorageManager(win, sanitizeStorageKey(props.storageKey));
    const enabled = props.enabledFeatures?.filter((key) => PREFERENCE_KEYS.includes(key)) ?? PREFERENCE_KEYS;
    this.manager = new PreferencesManager(this.storage.load(), enabled);
    this.sync = new SyncManager(win, this.storage, (prefs) => {
      this.remoteUpdate = true;
      try {
        this.manager.replace(prefs);
      } finally {
        this.remoteUpdate = false;
      }
    });
    const zIndex = Math.round(clampNumber(internal.zIndex, 0, 2_000_000, DEFAULT_Z_INDEX));
    this.engine = this.doc
      ? new PreferenceEngine(this.doc, {
        zIndex,
        readingGuide: resolveGuideOptions(props.readingGuideOptions),
        readingMask: resolveMaskOptions(props.readingMaskOptions),
      })
      : null;

    if (!this.doc || !this.engine) return;
    this.releaseStyles = acquireRuntimeStyles(this.doc, RUNTIME_CSS);
    this.engine.apply(this.manager.get());
    this.unsubscribe = this.manager.subscribe((next, previous) => {
      this.engine?.apply(next);
      if (!this.remoteUpdate) {
        if (isDefault(next)) this.storage.clear();
        else this.storage.save(next);
        this.sync.publish(next);
      }
      props.onPreferenceChange?.(next, previous);
      this.dispatch({ preferences: next, previous });
    });
    this.sync.start();
  }

  get isBrowser(): boolean {
    return this.doc !== null;
  }

  get syncMode(): 'broadcast' | 'storage' | 'none' {
    return this.sync.mode;
  }

  get storageKey(): string {
    return this.storage.key;
  }

  getPreferences(): AccessibilityPreferences {
    return this.manager.get();
  }

  isEnabled(key: PreferenceKey): boolean {
    return this.manager.isEnabled(key);
  }

  subscribe(listener: (next: AccessibilityPreferences, previous: AccessibilityPreferences) => void): Unsubscribe {
    return this.manager.subscribe(listener);
  }

  setPreference<K extends PreferenceKey>(key: K, value: AccessibilityPreferences[K]): void {
    this.manager.setPreference(key, value);
  }

  toggle(key: BooleanPreferenceKey): void {
    this.manager.toggle(key);
  }

  step(key: SteppedPreferenceKey, delta: 1 | -1): void {
    this.manager.step(key, delta);
  }

  setContrastMode(mode: ContrastMode | null): void {
    this.manager.setContrastMode(mode);
  }

  /** Restores every default, clears only this toolbar's storage key and tells other tabs. */
  reset(): void {
    const wasDefault = isDefault(this.manager.get());
    this.manager.reset();
    if (wasDefault) {
      this.storage.clear();
      this.sync.publish(defaultPreferences);
    }
  }

  /** Re-reads host stylesheets for text scaling, for pages that add CSS after load. */
  refresh(): void {
    this.engine?.refreshTextScale();
  }

  destroy(): void {
    if (this.destroyed) return;
    this.destroyed = true;
    this.unsubscribe();
    this.sync.stop();
    if (!this.doc) return;
    this.releaseStyles();
    if (runtimeStyleRefs(this.doc) === 0) this.engine?.clear();
  }

  private dispatch(detail: PreferencesListenerArgs): void {
    const win = getWindow(this.doc);
    if (!win || typeof win.CustomEvent !== 'function') return;
    try {
      win.dispatchEvent(new win.CustomEvent(PREFERENCE_EVENT, { detail }));
    } catch {
      /* Events are informational only. */
    }
  }
}
