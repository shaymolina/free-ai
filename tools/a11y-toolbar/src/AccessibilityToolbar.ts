import { AccessibilityProvider } from './AccessibilityProvider';
import { createTranslations, formatMessage, isToolbarLanguage } from './locales';
import { CONTRAST_MODES, activeContrastMode, preferencesEqual } from './preferences';
import type {
  AccessibilityPreferences,
  AccessibilityToolbarProps,
  BooleanPreferenceKey,
  ContrastMode,
  SteppedPreferenceKey,
  ToggleFeature,
  ToolbarDirection,
  ToolbarPosition,
  ToolbarTheme,
  ToolbarTranslations,
  Unsubscribe,
} from './types';
import { bodyOf, createId, getDocument, isSafeColor, listenMedia, safeMatchMedia } from './utils/browser';
import {
  AccessibilitySection,
  AccessibilityStepper,
  AccessibilityToggle,
  ContrastModeGroup,
  type Control,
  type ControlContext,
  ResetAccessibilityButton,
  formatStep,
} from './ui/controls';
import { el, joinClasses } from './ui/dom';
import type { IconName } from './ui/icons';
import { AccessibilityPanel, FloatingAccessibilityButton, LiveAnnouncer, type PanelParts } from './ui/parts';

export const ROOT_ID = 'a11y-toolbar-root';
const POSITIONS: readonly ToolbarPosition[] = ['bottom-right', 'bottom-left', 'top-right', 'top-left'];
const THEMES: readonly ToolbarTheme[] = ['light', 'dark', 'system'];

export interface AccessibilityToolbarController {
  readonly provider: AccessibilityProvider;
  readonly mounted: boolean;
  isOpen(): boolean;
  open(): void;
  close(returnFocus?: boolean): void;
  toggle(): void;
  destroy(): void;
}

const TEXT_TOGGLES: readonly [ToggleFeature, IconName][] = [['readableFont', 'font']];
const MOTION_TOGGLES: readonly [ToggleFeature, IconName][] = [['pauseAnimations', 'pause'], ['reduceMotion', 'motion']];
const READING_TOGGLES: readonly [ToggleFeature, IconName][] = [
  ['highlightLinks', 'link'], ['highlightHeadings', 'heading'], ['readingGuide', 'guide'], ['readingMask', 'mask'],
  ['largeCursor', 'cursor'], ['focusHighlight', 'focus'], ['hideImages', 'image'],
];
const STEPPERS: readonly [SteppedPreferenceKey, IconName][] = [
  ['textScale', 'text'], ['letterSpacing', 'spacing'], ['wordSpacing', 'spacing'], ['lineHeight', 'lineHeight'],
];

function describeChange(prev: AccessibilityPreferences, next: AccessibilityPreferences, t: ToolbarTranslations): string | null {
  if (preferencesEqual(prev, next)) return null;
  if (prev.textScale !== next.textScale) {
    const value = String(Math.round(next.textScale * 100));
    if (next.textScale === 1) return t.announceTextReset;
    return formatMessage(next.textScale > prev.textScale ? t.announceTextIncreased : t.announceTextDecreased, { value });
  }
  for (const key of ['letterSpacing', 'wordSpacing', 'lineHeight'] as const) {
    if (prev[key] !== next[key]) return formatMessage(t.announceValueChanged, { label: t[key], value: formatStep(key, next[key], t) });
  }
  const prevMode = activeContrastMode(prev);
  const nextMode = activeContrastMode(next);
  if (prevMode !== nextMode) return nextMode ? formatMessage(t.announceEnabled, { label: t[nextMode] }) : t.announceContrastOff;
  const toggles: readonly ToggleFeature[] = [...TEXT_TOGGLES, ...MOTION_TOGGLES, ...READING_TOGGLES].map(([key]) => key);
  for (const key of [...toggles, 'grayscale'] as const) {
    if (prev[key] !== next[key]) return formatMessage(next[key] ? t.announceEnabled : t.announceDisabled, { label: t[key] });
  }
  return null;
}

function noopController(provider: AccessibilityProvider): AccessibilityToolbarController {
  return {
    provider,
    mounted: false,
    isOpen: () => false,
    open: () => undefined,
    close: () => undefined,
    toggle: () => undefined,
    destroy: () => provider.destroy(),
  };
}

/**
 * Mounts the floating button, the panel and the live region, wired to an AccessibilityProvider.
 * Pass an existing provider to share state; otherwise one is created and owned by the toolbar.
 */
export function AccessibilityToolbar(
  props: AccessibilityToolbarProps = {},
  sharedProvider?: AccessibilityProvider,
): AccessibilityToolbarController {
  const doc = getDocument(props.document);
  const zIndex = typeof props.zIndex === 'number' && Number.isFinite(props.zIndex) ? Math.round(props.zIndex) : 95;
  const provider = sharedProvider ?? new AccessibilityProvider(props, { zIndex });
  const ownsProvider = !sharedProvider;
  if (!doc) return noopController(provider);
  if (!props.allowMultiple && doc.getElementById(ROOT_ID)) {
    return ownsProvider ? noopController(provider) : { ...noopController(provider), destroy: () => undefined };
  }

  const language = isToolbarLanguage(props.language) ? props.language : 'he';
  const direction: ToolbarDirection = props.direction === 'ltr' || props.direction === 'rtl'
    ? props.direction : language === 'he' ? 'rtl' : 'ltr';
  const position = POSITIONS.includes(props.position ?? 'bottom-right') ? props.position ?? 'bottom-right' : 'bottom-right';
  const theme = THEMES.includes(props.theme ?? 'light') ? props.theme ?? 'light' : 'light';
  const t = createTranslations(language, {
    ...props.translations,
    ...(props.panelTitle ? { panelTitle: props.panelTitle } : {}),
    ...(props.buttonLabel ? { accessibilityOptions: props.buttonLabel } : {}),
  });
  const uid = createId().replace(/[^\w-]/g, '').slice(0, 8);
  const ctx: ControlContext = { doc, t, uid };

  const root = el(doc, 'div', {
    className: joinClasses('a11y-toolbar-root', props.className),
    attrs: {
      dir: direction,
      lang: language,
      'data-a11y-toolbar-position': position,
      'data-a11y-toolbar-theme': theme,
      'data-a11y-toolbar-layout': 'popover',
      'data-a11y-toolbar-ignore-text-scale': '',
    },
  });
  if (!props.allowMultiple || !doc.getElementById(ROOT_ID)) root.id = ROOT_ID;
  root.style.setProperty('--a11y-toolbar-z', String(zIndex));
  if (isSafeColor(props.primaryColor)) root.style.setProperty('--a11y-toolbar-primary', props.primaryColor.trim());

  const button = FloatingAccessibilityButton(doc, t.accessibilityOptions, joinClasses('a11y-toolbar-trigger', props.buttonClassName));
  const parts: PanelParts = AccessibilityPanel(doc, t, t.panelTitle, joinClasses('a11y-toolbar-panel', props.panelClassName), uid);
  const live = new LiveAnnouncer(doc);
  const controls: Control[] = [];

  const act = (fn: () => void, message?: string): void => {
    const before = provider.getPreferences();
    fn();
    const after = provider.getPreferences();
    const text = message ?? describeChange(before, after, t);
    if (text && (message !== undefined || !preferencesEqual(before, after))) live.announce(text);
  };
  const onToggle = (key: BooleanPreferenceKey): void => act(() => provider.toggle(key));
  const onStep = (key: SteppedPreferenceKey, delta: 1 | -1): void => act(() => provider.step(key, delta));
  const onStepReset = (key: SteppedPreferenceKey): void => act(() => provider.setPreference(key, 1));
  const onContrast = (mode: ContrastMode | null): void => act(() => provider.setContrastMode(mode));

  const toggles = (list: readonly [ToggleFeature, IconName][]): HTMLElement[] => list
    .filter(([key]) => provider.isEnabled(key))
    .map(([key, icon]) => {
      const control = AccessibilityToggle(ctx, key, icon, onToggle);
      controls.push(control);
      return control.element;
    });
  const grid = (items: HTMLElement[]): HTMLElement | null => (items.length ? el(doc, 'div', { className: 'a11y-toolbar-grid' }, items) : null);

  const steppers = STEPPERS.filter(([key]) => provider.isEnabled(key)).map(([key, icon]) => {
    const control = AccessibilityStepper(ctx, key, icon, onStep, onStepReset);
    controls.push(control);
    return control.element;
  });
  const textToggles = grid(toggles(TEXT_TOGGLES));
  const sections: HTMLElement[] = [];
  if (steppers.length || textToggles) sections.push(AccessibilitySection(ctx, 'text', t.sectionText, [...steppers, ...(textToggles ? [textToggles] : [])]));

  const colorItems: HTMLElement[] = [];
  const modes = CONTRAST_MODES.filter((mode) => provider.isEnabled(mode));
  if (modes.length) {
    const group = ContrastModeGroup(ctx, modes, onContrast);
    controls.push(group);
    colorItems.push(group.element);
  }
  if (provider.isEnabled('grayscale')) {
    const gray = AccessibilityToggle(ctx, 'grayscale', 'grayscale', onToggle);
    controls.push(gray);
    colorItems.push(el(doc, 'div', { className: 'a11y-toolbar-grid' }, [gray.element]));
  }
  if (colorItems.length) sections.push(AccessibilitySection(ctx, 'color', t.sectionColor, colorItems));
  const motion = grid(toggles(MOTION_TOGGLES));
  if (motion) sections.push(AccessibilitySection(ctx, 'motion', t.sectionMotion, [motion]));
  const reading = grid(toggles(READING_TOGGLES));
  if (reading) sections.push(AccessibilitySection(ctx, 'reading', t.sectionReading, [reading]));
  for (const section of sections) parts.body.appendChild(section);

  const reset = ResetAccessibilityButton(ctx, () => {
    act(() => provider.reset(), t.resetDone);
    if (props.closeOnReset) close(true);
    else reset.focus();
  });
  parts.footer.append(reset, el(doc, 'p', { className: 'a11y-toolbar-disclaimer', text: t.disclaimer }));
  root.append(button, parts.panel, live.element);

  const render = (prefs: AccessibilityPreferences): void => {
    for (const control of controls) control.update(prefs);
  };
  render(provider.getPreferences());
  const stopRender: Unsubscribe = provider.subscribe((next) => render(next));

  let open = false;
  const setOpen = (next: boolean, returnFocus: boolean): void => {
    if (next === open) return;
    open = next;
    parts.panel.hidden = !next;
    root.toggleAttribute('data-a11y-toolbar-open', next);
    button.setAttribute('aria-expanded', String(next));
    if (next) parts.title.focus({ preventScroll: true });
    else if (returnFocus) button.focus({ preventScroll: true });
    try {
      props.onOpenChange?.(next);
    } catch {
      /* Host callbacks must not break the toolbar. */
    }
  };
  function close(returnFocus = true): void {
    setOpen(false, returnFocus);
  }

  button.addEventListener('click', () => setOpen(!open, true));
  parts.close.addEventListener('click', () => close(true));

  const navigable = (): HTMLElement[] => Array.from(parts.panel.querySelectorAll<HTMLElement>('.a11y-toolbar-nav'));
  const onKeyDown = (event: KeyboardEvent): void => {
    if (event.key === 'Escape' && open) {
      event.preventDefault();
      event.stopPropagation();
      close(true);
      return;
    }
    const target = event.target;
    if (!(target instanceof HTMLElement) || !parts.panel.contains(target) || !target.classList.contains('a11y-toolbar-nav')) return;
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const items = navigable();
    const index = items.indexOf(target);
    let next: HTMLElement | undefined;
    if (event.key === 'ArrowDown') next = items[(index + 1) % items.length];
    else if (event.key === 'ArrowUp') next = items[(index - 1 + items.length) % items.length];
    else if (event.key === 'Home') next = items[0];
    else if (event.key === 'End') next = items[items.length - 1];
    if (next) {
      event.preventDefault();
      next.focus();
    }
  };
  root.addEventListener('keydown', onKeyDown);

  const onPointerDown = (event: PointerEvent): void => {
    if (!open || parts.panel.contains(event.target as Node) || button.contains(event.target as Node)) return;
    // Only the popover closes on outside clicks; the bottom sheet has its own close button.
    if (root.getAttribute('data-a11y-toolbar-layout') === 'popover') close(false);
  };
  doc.addEventListener('pointerdown', onPointerDown, true);

  const win = doc.defaultView;
  const breakpoint = typeof props.mobileBreakpoint === 'number' && props.mobileBreakpoint > 0 ? Math.round(props.mobileBreakpoint) : 640;
  const sheetQuery = safeMatchMedia(win, `(max-width: ${breakpoint}px)`);
  const updateLayout = (): void => root.setAttribute('data-a11y-toolbar-layout', sheetQuery?.matches ? 'sheet' : 'popover');
  updateLayout();
  const stopMedia = listenMedia(sheetQuery, updateLayout);

  let attached = false;
  const attach = (): void => {
    const body = bodyOf(doc);
    if (attached || !body) return;
    attached = true;
    body.appendChild(root);
    if (props.defaultOpen) setOpen(true, false);
  };
  if (bodyOf(doc)) attach();
  else doc.addEventListener('DOMContentLoaded', attach, { once: true });

  let destroyed = false;
  return {
    provider,
    mounted: true,
    isOpen: () => open,
    open: () => setOpen(true, false),
    close: (returnFocus = true) => close(returnFocus),
    toggle: () => setOpen(!open, true),
    destroy: () => {
      if (destroyed) return;
      destroyed = true;
      doc.removeEventListener('DOMContentLoaded', attach);
      doc.removeEventListener('pointerdown', onPointerDown, true);
      root.removeEventListener('keydown', onKeyDown);
      stopMedia();
      stopRender();
      live.destroy();
      root.remove();
      if (ownsProvider) provider.destroy();
    },
  };
}

/** Creates a provider and a toolbar in one call. */
export function createAccessibilityToolbar(props: AccessibilityToolbarProps = {}): AccessibilityToolbarController {
  return AccessibilityToolbar(props);
}
