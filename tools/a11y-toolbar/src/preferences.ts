import type {
  AccessibilityPreferences,
  BooleanPreferenceKey,
  ContrastMode,
  LetterSpacing,
  LineHeight,
  PreferenceKey,
  SteppedPreferenceKey,
  TextScale,
  Unsubscribe,
  WordSpacing,
} from './types';

export const TEXT_SCALES: readonly TextScale[] = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6];
export const LETTER_SPACINGS: readonly LetterSpacing[] = [0, 0.05, 0.1, 0.15];
export const WORD_SPACINGS: readonly WordSpacing[] = [0, 0.1, 0.2, 0.3];
export const LINE_HEIGHTS: readonly LineHeight[] = [0, 1.5, 1.75, 2];

/** Deterministic precedence: when stored data has several contrast modes on, the first one wins. */
export const CONTRAST_MODES: readonly ContrastMode[] = ['highContrast', 'darkContrast', 'lightContrast', 'invertColors'];

export const defaultPreferences: AccessibilityPreferences = Object.freeze({
  textScale: 1,
  readableFont: false,
  letterSpacing: 0,
  wordSpacing: 0,
  lineHeight: 0,
  pauseAnimations: false,
  reduceMotion: false,
  grayscale: false,
  highContrast: false,
  darkContrast: false,
  lightContrast: false,
  invertColors: false,
  highlightLinks: false,
  highlightHeadings: false,
  readingGuide: false,
  readingMask: false,
  largeCursor: false,
  focusHighlight: false,
  hideImages: false,
});

export const PREFERENCE_KEYS = Object.keys(defaultPreferences) as readonly PreferenceKey[];

export const BOOLEAN_KEYS: readonly BooleanPreferenceKey[] = [
  'readableFont', 'pauseAnimations', 'reduceMotion', 'grayscale', 'highContrast', 'darkContrast',
  'lightContrast', 'invertColors', 'highlightLinks', 'highlightHeadings', 'readingGuide', 'readingMask',
  'largeCursor', 'focusHighlight', 'hideImages',
];

export type StepValue<K extends SteppedPreferenceKey> = AccessibilityPreferences[K];

export const STEPS: { readonly [K in SteppedPreferenceKey]: readonly AccessibilityPreferences[K][] } = {
  textScale: TEXT_SCALES,
  letterSpacing: LETTER_SPACINGS,
  wordSpacing: WORD_SPACINGS,
  lineHeight: LINE_HEIGHTS,
};

export function isSteppedKey(key: PreferenceKey): key is SteppedPreferenceKey {
  return key === 'textScale' || key === 'letterSpacing' || key === 'wordSpacing' || key === 'lineHeight';
}

export function isContrastMode(key: PreferenceKey): key is ContrastMode {
  return (CONTRAST_MODES as readonly PreferenceKey[]).includes(key);
}

function isStepValue<K extends SteppedPreferenceKey>(key: K, value: unknown): value is AccessibilityPreferences[K] {
  return typeof value === 'number' && (STEPS[key] as readonly number[]).includes(value);
}

export function isRecord(value: unknown): value is Readonly<Record<string, unknown>> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/** Builds a valid preference object from unknown input. Unknown fields are dropped, invalid values fall back to defaults. */
export function sanitizePreferences(input: unknown): AccessibilityPreferences {
  if (!isRecord(input)) return defaultPreferences;
  const out: { -readonly [K in PreferenceKey]: AccessibilityPreferences[K] } = { ...defaultPreferences };
  for (const key of BOOLEAN_KEYS) {
    const value = input[key];
    if (typeof value === 'boolean') out[key] = value;
  }
  const textScale = input.textScale;
  if (isStepValue('textScale', textScale)) out.textScale = textScale;
  const letterSpacing = input.letterSpacing;
  if (isStepValue('letterSpacing', letterSpacing)) out.letterSpacing = letterSpacing;
  const wordSpacing = input.wordSpacing;
  if (isStepValue('wordSpacing', wordSpacing)) out.wordSpacing = wordSpacing;
  const lineHeight = input.lineHeight;
  if (isStepValue('lineHeight', lineHeight)) out.lineHeight = lineHeight;
  const winner = CONTRAST_MODES.find((mode) => out[mode]);
  for (const mode of CONTRAST_MODES) out[mode] = mode === winner;
  return Object.freeze(out);
}

export function activeContrastMode(prefs: AccessibilityPreferences): ContrastMode | null {
  return CONTRAST_MODES.find((mode) => prefs[mode]) ?? null;
}

export function preferencesEqual(a: AccessibilityPreferences, b: AccessibilityPreferences): boolean {
  return PREFERENCE_KEYS.every((key) => a[key] === b[key]);
}

export function isDefault(prefs: AccessibilityPreferences): boolean {
  return preferencesEqual(prefs, defaultPreferences);
}

export function stepIndex<K extends SteppedPreferenceKey>(key: K, value: AccessibilityPreferences[K]): number {
  return (STEPS[key] as readonly number[]).indexOf(value);
}

/** Returns the neighbouring step, clamped to the list. */
export function nextStep<K extends SteppedPreferenceKey>(
  key: K,
  value: AccessibilityPreferences[K],
  delta: 1 | -1,
): AccessibilityPreferences[K] {
  const list = STEPS[key];
  const index = Math.min(list.length - 1, Math.max(0, stepIndex(key, value) + delta));
  const step = list[index];
  return step === undefined ? value : step;
}

export type PreferencesListener = (next: AccessibilityPreferences, previous: AccessibilityPreferences) => void;

/** Owns the single immutable preference state. Every write goes through `set`, which validates and enforces contrast exclusivity. */
export class PreferencesManager {
  private state: AccessibilityPreferences;
  private readonly listeners = new Set<PreferencesListener>();
  private readonly enabled: ReadonlySet<PreferenceKey>;

  constructor(initial: AccessibilityPreferences = defaultPreferences, enabled: readonly PreferenceKey[] = PREFERENCE_KEYS) {
    this.enabled = new Set(enabled);
    this.state = this.restrict(sanitizePreferences(initial));
  }

  get(): AccessibilityPreferences {
    return this.state;
  }

  isEnabled(key: PreferenceKey): boolean {
    return this.enabled.has(key);
  }

  subscribe(listener: PreferencesListener): Unsubscribe {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  setPreference<K extends PreferenceKey>(key: K, value: AccessibilityPreferences[K]): void {
    if (!this.enabled.has(key)) return;
    const patch: Partial<Record<PreferenceKey, unknown>> = { [key]: value };
    if (isContrastMode(key) && value === true) {
      for (const mode of CONTRAST_MODES) if (mode !== key) patch[mode] = false;
    }
    this.replace({ ...this.state, ...patch });
  }

  setContrastMode(mode: ContrastMode | null): void {
    const patch: Partial<Record<ContrastMode, boolean>> = {};
    for (const m of CONTRAST_MODES) patch[m] = m === mode && this.enabled.has(m);
    this.replace({ ...this.state, ...patch });
  }

  toggle(key: BooleanPreferenceKey): void {
    this.setPreference(key, !this.state[key]);
  }

  step(key: SteppedPreferenceKey, delta: 1 | -1): void {
    switch (key) {
      case 'textScale': this.setPreference(key, nextStep(key, this.state.textScale, delta)); break;
      case 'letterSpacing': this.setPreference(key, nextStep(key, this.state.letterSpacing, delta)); break;
      case 'wordSpacing': this.setPreference(key, nextStep(key, this.state.wordSpacing, delta)); break;
      case 'lineHeight': this.setPreference(key, nextStep(key, this.state.lineHeight, delta)); break;
    }
  }

  reset(): void {
    this.replace(defaultPreferences);
  }

  /** Replaces the whole state (used for storage loads and cross-tab updates). */
  replace(next: unknown): void {
    const clean = this.restrict(sanitizePreferences(next));
    if (preferencesEqual(clean, this.state)) return;
    const previous = this.state;
    this.state = clean;
    for (const listener of [...this.listeners]) {
      try {
        listener(clean, previous);
      } catch {
        /* A failing listener must not break the others or the host page. */
      }
    }
  }

  private restrict(prefs: AccessibilityPreferences): AccessibilityPreferences {
    if (this.enabled.size === PREFERENCE_KEYS.length) return prefs;
    const out: Record<string, unknown> = { ...prefs };
    for (const key of PREFERENCE_KEYS) if (!this.enabled.has(key)) out[key] = defaultPreferences[key];
    return sanitizePreferences(out);
  }
}
