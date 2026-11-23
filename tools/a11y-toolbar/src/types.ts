export type TextScale = 1 | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 | 1.6;
export type LetterSpacing = 0 | 0.05 | 0.1 | 0.15;
export type WordSpacing = 0 | 0.1 | 0.2 | 0.3;
export type LineHeight = 0 | 1.5 | 1.75 | 2;

export interface AccessibilityPreferences {
  readonly textScale: TextScale;
  readonly readableFont: boolean;
  readonly letterSpacing: LetterSpacing;
  readonly wordSpacing: WordSpacing;
  readonly lineHeight: LineHeight;
  readonly pauseAnimations: boolean;
  readonly reduceMotion: boolean;
  readonly grayscale: boolean;
  readonly highContrast: boolean;
  readonly darkContrast: boolean;
  readonly lightContrast: boolean;
  readonly invertColors: boolean;
  readonly highlightLinks: boolean;
  readonly highlightHeadings: boolean;
  readonly readingGuide: boolean;
  readonly readingMask: boolean;
  readonly largeCursor: boolean;
  readonly focusHighlight: boolean;
  readonly hideImages: boolean;
}

export type PreferenceKey = keyof AccessibilityPreferences;

export type BooleanPreferenceKey = {
  [K in PreferenceKey]: AccessibilityPreferences[K] extends boolean ? K : never;
}[PreferenceKey];

export type SteppedPreferenceKey = Exclude<PreferenceKey, BooleanPreferenceKey>;

export type ContrastMode = 'highContrast' | 'darkContrast' | 'lightContrast' | 'invertColors';

export type ToggleFeature = Exclude<BooleanPreferenceKey, ContrastMode>;

export type ToolbarFeature = PreferenceKey;

export type ToolbarPosition = 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
export type ToolbarDirection = 'rtl' | 'ltr';
export type ToolbarLanguage = 'he' | 'en';
export type ToolbarTheme = 'light' | 'dark' | 'system';

export interface ReadingGuideOptions {
  readonly color?: string;
  readonly thickness?: number;
  readonly followFocus?: boolean;
}

export interface ReadingMaskOptions {
  readonly opacity?: number;
  readonly areaHeight?: number;
  readonly followFocus?: boolean;
}

export interface ResolvedReadingGuideOptions {
  readonly color: string;
  readonly thickness: number;
  readonly followFocus: boolean;
}

export interface ResolvedReadingMaskOptions {
  readonly opacity: number;
  readonly areaHeight: number;
  readonly followFocus: boolean;
}

export interface ToolbarTranslations {
  readonly accessibilityOptions: string;
  readonly panelTitle: string;
  readonly panelDescription: string;
  readonly close: string;
  readonly active: string;
  readonly inactive: string;
  readonly on: string;
  readonly off: string;
  readonly normal: string;
  readonly percent: string;
  readonly sectionText: string;
  readonly sectionColor: string;
  readonly sectionMotion: string;
  readonly sectionReading: string;
  readonly contrastGroup: string;
  readonly contrastNone: string;
  readonly textScale: string;
  readonly increaseText: string;
  readonly decreaseText: string;
  readonly resetText: string;
  readonly readableFont: string;
  readonly letterSpacing: string;
  readonly increaseLetterSpacing: string;
  readonly decreaseLetterSpacing: string;
  readonly wordSpacing: string;
  readonly increaseWordSpacing: string;
  readonly decreaseWordSpacing: string;
  readonly lineHeight: string;
  readonly increaseLineHeight: string;
  readonly decreaseLineHeight: string;
  readonly pauseAnimations: string;
  readonly reduceMotion: string;
  readonly grayscale: string;
  readonly highContrast: string;
  readonly darkContrast: string;
  readonly lightContrast: string;
  readonly invertColors: string;
  readonly highlightLinks: string;
  readonly highlightHeadings: string;
  readonly readingGuide: string;
  readonly readingMask: string;
  readonly largeCursor: string;
  readonly focusHighlight: string;
  readonly hideImages: string;
  readonly resetAll: string;
  readonly resetDone: string;
  readonly announceEnabled: string;
  readonly announceDisabled: string;
  readonly announceTextIncreased: string;
  readonly announceTextDecreased: string;
  readonly announceTextReset: string;
  readonly announceValueChanged: string;
  readonly announceContrastOff: string;
  readonly disclaimer: string;
}

export type PartialTranslations = Partial<ToolbarTranslations>;

export type PreferenceChangeHandler = (
  preferences: AccessibilityPreferences,
  previous: AccessibilityPreferences,
) => void;

export type OpenChangeHandler = (isOpen: boolean) => void;

export interface AccessibilityProviderProps {
  readonly storageKey?: string;
  readonly enabledFeatures?: readonly ToolbarFeature[];
  readonly readingGuideOptions?: ReadingGuideOptions;
  readonly readingMaskOptions?: ReadingMaskOptions;
  readonly onPreferenceChange?: PreferenceChangeHandler;
  readonly document?: Document;
}

export interface AccessibilityToolbarProps extends AccessibilityProviderProps {
  readonly language?: ToolbarLanguage;
  readonly direction?: ToolbarDirection;
  readonly position?: ToolbarPosition;
  readonly primaryColor?: string;
  readonly zIndex?: number;
  readonly defaultOpen?: boolean;
  readonly translations?: PartialTranslations;
  readonly panelTitle?: string;
  readonly buttonLabel?: string;
  readonly theme?: ToolbarTheme;
  readonly className?: string;
  readonly buttonClassName?: string;
  readonly panelClassName?: string;
  readonly closeOnReset?: boolean;
  readonly allowMultiple?: boolean;
  readonly mobileBreakpoint?: number;
  readonly onOpenChange?: OpenChangeHandler;
}

export interface StoredPreferencesV1 {
  readonly version: 1;
  readonly preferences: AccessibilityPreferences;
}

export interface SyncMessage {
  readonly namespace: 'a11y-toolbar';
  readonly version: 1;
  readonly source: string;
  readonly preferences: AccessibilityPreferences;
}

export type Unsubscribe = () => void;

export interface PreferencesListenerArgs {
  readonly preferences: AccessibilityPreferences;
  readonly previous: AccessibilityPreferences;
}
