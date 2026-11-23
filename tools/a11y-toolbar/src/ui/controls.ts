import type {
  AccessibilityPreferences,
  BooleanPreferenceKey,
  ContrastMode,
  SteppedPreferenceKey,
  ToolbarTranslations,
} from '../types';
import { CONTRAST_MODES, STEPS, activeContrastMode, stepIndex } from '../preferences';
import { el } from './dom';
import { type IconName, createIcon } from './icons';

export interface Control {
  readonly element: HTMLElement;
  update(prefs: AccessibilityPreferences): void;
}

export interface ControlContext {
  readonly doc: Document;
  readonly t: ToolbarTranslations;
  readonly uid: string;
}

/** A titled group of controls. */
export function AccessibilitySection(ctx: ControlContext, key: string, title: string, children: readonly HTMLElement[]): HTMLElement {
  const headingId = `a11y-toolbar-${ctx.uid}-section-${key}`;
  return el(ctx.doc, 'section', { className: 'a11y-toolbar-section', attrs: { 'aria-labelledby': headingId } }, [
    el(ctx.doc, 'h3', { className: 'a11y-toolbar-section-title', id: headingId, text: title }),
    el(ctx.doc, 'div', { className: 'a11y-toolbar-section-body' }, children),
  ]);
}

/** On/off preference as a native button with aria-pressed. The visible state text is redundant for screen readers, so it is hidden from them. */
export function AccessibilityToggle(
  ctx: ControlContext,
  key: BooleanPreferenceKey,
  icon: IconName,
  onToggle: (key: BooleanPreferenceKey) => void,
): Control {
  const { doc, t } = ctx;
  const stateText = el(doc, 'span', { className: 'a11y-toolbar-toggle-state-text', text: t.inactive });
  const button = el(doc, 'button', {
    className: 'a11y-toolbar-toggle a11y-toolbar-nav',
    attrs: { type: 'button', 'aria-pressed': 'false', 'data-a11y-toolbar-control': key },
  }, [
    createIcon(doc, icon),
    el(doc, 'span', { className: 'a11y-toolbar-toggle-label', text: t[key] }),
    el(doc, 'span', { className: 'a11y-toolbar-toggle-state', attrs: { 'aria-hidden': 'true' } }, [
      createIcon(doc, 'check', 'a11y-toolbar-icon a11y-toolbar-check'),
      stateText,
    ]),
  ]);
  button.addEventListener('click', () => onToggle(key));
  return {
    element: button,
    update(prefs) {
      const on = prefs[key];
      button.setAttribute('aria-pressed', String(on));
      stateText.textContent = on ? t.active : t.inactive;
    },
  };
}

export function formatStep(key: SteppedPreferenceKey, value: number, t: ToolbarTranslations): string {
  if (key === 'textScale') return `${Math.round(value * 100)}%`;
  if (value === 0) return t.normal;
  if (key === 'lineHeight') return String(value);
  const index = (STEPS[key] as readonly number[]).indexOf(value);
  return `+${index}`;
}

interface StepperLabels {
  readonly label: string;
  readonly decrease: string;
  readonly increase: string;
  readonly reset?: string;
}

function stepperLabels(key: SteppedPreferenceKey, t: ToolbarTranslations): StepperLabels {
  switch (key) {
    case 'textScale': return { label: t.textScale, decrease: t.decreaseText, increase: t.increaseText, reset: t.resetText };
    case 'letterSpacing': return { label: t.letterSpacing, decrease: t.decreaseLetterSpacing, increase: t.increaseLetterSpacing };
    case 'wordSpacing': return { label: t.wordSpacing, decrease: t.decreaseWordSpacing, increase: t.increaseWordSpacing };
    case 'lineHeight': return { label: t.lineHeight, decrease: t.decreaseLineHeight, increase: t.increaseLineHeight };
  }
}

/** One icon action button inside a stepper. aria-disabled keeps it focusable at the limits. */
export function AccessibilityControlButton(
  ctx: ControlContext,
  icon: IconName,
  label: string,
  describedBy: string,
  onPress: () => void,
): HTMLButtonElement {
  const button = el(ctx.doc, 'button', {
    className: 'a11y-toolbar-step-button a11y-toolbar-nav',
    attrs: { type: 'button', 'aria-label': label, title: label, 'aria-describedby': describedBy },
  }, [createIcon(ctx.doc, icon)]);
  button.addEventListener('click', () => {
    if (button.getAttribute('aria-disabled') !== 'true') onPress();
  });
  return button;
}

/** Stepped value with decrease and increase buttons and a visible current value. */
export function AccessibilityStepper(
  ctx: ControlContext,
  key: SteppedPreferenceKey,
  icon: IconName,
  onStep: (key: SteppedPreferenceKey, delta: 1 | -1) => void,
  onReset: (key: SteppedPreferenceKey) => void,
): Control {
  const { doc, t, uid } = ctx;
  const labels = stepperLabels(key, t);
  const labelId = `a11y-toolbar-${uid}-${key}-label`;
  const valueId = `a11y-toolbar-${uid}-${key}-value`;
  const value = el(doc, 'bdi', { className: 'a11y-toolbar-step-value', id: valueId });
  const decrease = AccessibilityControlButton(ctx, 'minus', labels.decrease, valueId, () => onStep(key, -1));
  const increase = AccessibilityControlButton(ctx, 'plus', labels.increase, valueId, () => onStep(key, 1));
  decrease.setAttribute('data-a11y-toolbar-control', `${key}-decrease`);
  increase.setAttribute('data-a11y-toolbar-control', `${key}-increase`);
  let reset: HTMLButtonElement | null = null;
  if (labels.reset) {
    reset = el(doc, 'button', {
      className: 'a11y-toolbar-step-reset a11y-toolbar-nav',
      text: t.normal,
      attrs: { type: 'button', 'aria-label': labels.reset, 'data-a11y-toolbar-control': `${key}-reset` },
    });
    const btn = reset;
    btn.addEventListener('click', () => {
      if (btn.getAttribute('aria-disabled') !== 'true') onReset(key);
    });
  }
  const element = el(doc, 'div', {
    className: 'a11y-toolbar-stepper',
    attrs: { role: 'group', 'aria-labelledby': labelId, 'data-a11y-toolbar-stepper': key },
  }, [
    el(doc, 'span', { className: 'a11y-toolbar-stepper-label' }, [
      createIcon(doc, icon),
      el(doc, 'span', { id: labelId, text: labels.label }),
    ]),
    el(doc, 'span', { className: 'a11y-toolbar-stepper-controls' }, [decrease, value, increase, reset]),
  ]);
  return {
    element,
    update(prefs) {
      const current = prefs[key];
      const index = stepIndex(key, current);
      const last = STEPS[key].length - 1;
      value.textContent = formatStep(key, current, t);
      decrease.setAttribute('aria-disabled', String(index <= 0));
      increase.setAttribute('aria-disabled', String(index >= last));
      reset?.setAttribute('aria-disabled', String(index <= 0));
      element.toggleAttribute('data-a11y-toolbar-changed', index > 0);
    },
  };
}

/** The mutually exclusive contrast modes, as a native radio group. */
export function ContrastModeGroup(
  ctx: ControlContext,
  modes: readonly ContrastMode[],
  onSelect: (mode: ContrastMode | null) => void,
): Control {
  const { doc, t, uid } = ctx;
  const name = `a11y-toolbar-${uid}-contrast`;
  const inputs = new Map<ContrastMode | 'none', HTMLInputElement>();
  const option = (mode: ContrastMode | 'none', label: string): HTMLLabelElement => {
    const input = el(doc, 'input', {
      className: 'a11y-toolbar-radio-input',
      attrs: { type: 'radio', name, value: mode, 'data-a11y-toolbar-control': `contrast-${mode}` },
    });
    input.addEventListener('change', () => {
      if (input.checked) onSelect(mode === 'none' ? null : mode);
    });
    inputs.set(mode, input);
    return el(doc, 'label', { className: 'a11y-toolbar-radio' }, [
      input,
      el(doc, 'span', { className: 'a11y-toolbar-radio-mark', attrs: { 'aria-hidden': 'true' } }),
      el(doc, 'span', { className: 'a11y-toolbar-radio-label', text: label }),
    ]);
  };
  const ordered = CONTRAST_MODES.filter((mode) => modes.includes(mode));
  const element = el(doc, 'fieldset', { className: 'a11y-toolbar-radios' }, [
    el(doc, 'legend', { className: 'a11y-toolbar-radios-legend', text: t.contrastGroup }),
    el(doc, 'div', { className: 'a11y-toolbar-radios-grid' }, [
      option('none', t.contrastNone),
      ...ordered.map((mode) => option(mode, t[mode])),
    ]),
  ]);
  return {
    element,
    update(prefs) {
      const active = activeContrastMode(prefs) ?? 'none';
      for (const [mode, input] of inputs) input.checked = mode === active;
    },
  };
}

export function ResetAccessibilityButton(ctx: ControlContext, onReset: () => void): HTMLButtonElement {
  const button = el(ctx.doc, 'button', {
    className: 'a11y-toolbar-reset a11y-toolbar-nav',
    attrs: { type: 'button', 'data-a11y-toolbar-control': 'reset' },
  }, [createIcon(ctx.doc, 'reset'), el(ctx.doc, 'span', { text: ctx.t.resetAll })]);
  button.addEventListener('click', onReset);
  return button;
}
