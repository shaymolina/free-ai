import { afterEach, describe, expect, it, vi } from 'vitest';
import { createAccessibilityToolbar, type AccessibilityToolbarController } from '../../src/AccessibilityToolbar';
import { AccessibilityProvider } from '../../src/AccessibilityProvider';
import { AccessibilityToolbar } from '../../src/AccessibilityToolbar';
import { DEFAULT_STORAGE_KEY } from '../../src/managers/StorageManager';
import { RUNTIME_STYLE_ID } from '../../src/managers/StyleManager';
import { defaultPreferences } from '../../src/preferences';
import type { AccessibilityToolbarProps } from '../../src/types';

const mounted: AccessibilityToolbarController[] = [];

function mount(props: AccessibilityToolbarProps = {}): AccessibilityToolbarController {
  const toolbar = createAccessibilityToolbar(props);
  mounted.push(toolbar);
  return toolbar;
}

const trigger = (): HTMLButtonElement => {
  const el = document.getElementById('a11y-toolbar-trigger');
  if (!(el instanceof HTMLButtonElement)) throw new Error('trigger missing');
  return el;
};
const panel = (): HTMLElement => {
  const el = document.getElementById('a11y-panel');
  if (!el) throw new Error('panel missing');
  return el;
};
const control = (name: string): HTMLElement => {
  const el = document.querySelector<HTMLElement>(`[data-a11y-toolbar-control="${name}"]`);
  if (!el) throw new Error(`control ${name} missing`);
  return el;
};
const html = (): HTMLElement => document.documentElement;

afterEach(() => {
  for (const toolbar of mounted.splice(0)) toolbar.destroy();
  localStorage.clear();
  vi.useRealTimers();
});

describe('floating button', () => {
  it('renders with the required semantics', () => {
    mount();
    const button = trigger();
    expect(button.type).toBe('button');
    expect(button.getAttribute('aria-expanded')).toBe('false');
    expect(button.getAttribute('aria-controls')).toBe('a11y-panel');
    expect(button.getAttribute('aria-haspopup')).toBe('dialog');
    expect(button.getAttribute('aria-label')).toBe('אפשרויות נגישות');
    expect(button.getAttribute('title')).toBe('אפשרויות נגישות');
    expect(button.textContent).toBe('');
    expect(document.getElementById(button.getAttribute('aria-controls') ?? '')).toBe(panel());
  });

  it('uses the exact Lucide accessibility icon, decorative and inheriting currentColor', () => {
    mount();
    const svg = trigger().querySelector('svg');
    expect(svg?.getAttribute('aria-hidden')).toBe('true');
    expect(svg?.getAttribute('focusable')).toBe('false');
    expect(svg?.getAttribute('viewBox')).toBe('0 0 24 24');
    expect(svg?.getAttribute('stroke')).toBe('currentColor');
    expect(svg?.getAttribute('fill')).toBe('none');
    expect(svg?.getAttribute('stroke-width')).toBe('2');
    const circle = svg?.querySelector('circle');
    expect([circle?.getAttribute('cx'), circle?.getAttribute('cy'), circle?.getAttribute('r')]).toEqual(['16', '4', '1']);
    expect(Array.from(svg?.querySelectorAll('path') ?? []).map((p) => p.getAttribute('d'))).toEqual([
      'm18 19 1-7-6 1', 'm5 8 3-3 5.5 3-2.36 3.5', 'M4.24 14.5a5 5 0 0 0 6.88 6', 'M13.76 17.5a5 5 0 0 0-6.88-6',
    ]);
  });

  it('uses English labels and LTR direction for English', () => {
    mount({ language: 'en' });
    expect(trigger().getAttribute('aria-label')).toBe('Accessibility options');
    expect(document.querySelector('.a11y-toolbar-root')?.getAttribute('dir')).toBe('ltr');
    expect(document.querySelector('.a11y-toolbar-root')?.getAttribute('lang')).toBe('en');
  });

  it('uses RTL for Hebrew and honours an explicit direction', () => {
    const first = mount();
    expect(document.querySelector('.a11y-toolbar-root')?.getAttribute('dir')).toBe('rtl');
    first.destroy();
    mount({ language: 'he', direction: 'ltr' });
    expect(document.querySelector('.a11y-toolbar-root')?.getAttribute('dir')).toBe('ltr');
  });

  it('applies position, theme, z-index and a safe primary color; rejects unsafe color', () => {
    mount({ position: 'top-left', theme: 'dark', zIndex: 500, primaryColor: '#123456' });
    const root = document.querySelector<HTMLElement>('.a11y-toolbar-root');
    expect(root?.getAttribute('data-a11y-toolbar-position')).toBe('top-left');
    expect(root?.getAttribute('data-a11y-toolbar-theme')).toBe('dark');
    expect(root?.style.getPropertyValue('--a11y-toolbar-z')).toBe('500');
    expect(root?.style.getPropertyValue('--a11y-toolbar-primary')).toBe('#123456');
    mounted.splice(0).forEach((t) => t.destroy());
    mount({ primaryColor: 'red;}body{display:none' });
    expect(document.querySelector<HTMLElement>('.a11y-toolbar-root')?.style.getPropertyValue('--a11y-toolbar-primary')).toBe('');
  });

  it('defaults to bottom-right', () => {
    mount();
    expect(document.querySelector('.a11y-toolbar-root')?.getAttribute('data-a11y-toolbar-position')).toBe('bottom-right');
  });
});

describe('panel', () => {
  it('opens and closes, updating aria-expanded and focus', () => {
    const onOpenChange = vi.fn();
    mount({ onOpenChange });
    expect(panel().hidden).toBe(true);
    trigger().click();
    expect(panel().hidden).toBe(false);
    expect(trigger().getAttribute('aria-expanded')).toBe('true');
    expect(document.activeElement?.id).toBe(panel().getAttribute('aria-labelledby'));
    control('close').click();
    expect(panel().hidden).toBe(true);
    expect(trigger().getAttribute('aria-expanded')).toBe('false');
    expect(document.activeElement).toBe(trigger());
    expect(onOpenChange.mock.calls).toEqual([[true], [false]]);
  });

  it('is a non-modal dialog with a visible title and a localized close button', () => {
    mount();
    expect(panel().getAttribute('role')).toBe('dialog');
    expect(panel().getAttribute('aria-modal')).toBe('false');
    const title = document.getElementById(panel().getAttribute('aria-labelledby') ?? '');
    expect(title?.textContent).toBe('תפריט נגישות');
    expect(control('close').getAttribute('aria-label')).toBe('סגירת תפריט הנגישות');
    expect(control('close').querySelector('svg')).not.toBeNull();
  });

  it('closes on Escape and returns focus to the button', () => {
    mount();
    trigger().click();
    control('readableFont').focus();
    control('readableFont').dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    expect(panel().hidden).toBe(true);
    expect(document.activeElement).toBe(trigger());
  });

  it('supports arrow, Home and End navigation between controls', () => {
    mount();
    trigger().click();
    const items = Array.from(panel().querySelectorAll<HTMLElement>('.a11y-toolbar-nav'));
    const first = items[0];
    const last = items[items.length - 1];
    if (!first || !last) throw new Error('no controls');
    first.focus();
    first.dispatchEvent(new KeyboardEvent('keydown', { key: 'End', bubbles: true }));
    expect(document.activeElement).toBe(last);
    last.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
    expect(document.activeElement).toBe(first);
    first.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowUp', bubbles: true }));
    expect(document.activeElement).toBe(last);
    last.dispatchEvent(new KeyboardEvent('keydown', { key: 'Home', bubbles: true }));
    expect(document.activeElement).toBe(first);
  });

  it('honours defaultOpen', () => {
    mount({ defaultOpen: true });
    expect(panel().hidden).toBe(false);
  });

  it('contains no scanner, checker, audit, issues or score features', () => {
    mount({ language: 'en' });
    const text = (document.querySelector('.a11y-toolbar-root')?.textContent ?? '').toLowerCase();
    for (const word of ['scanner', 'scan', 'inspector', 'checker', 'audit', 'issues', 'errors', 'score', 'compliance', 'violation']) {
      expect(text).not.toContain(word);
    }
    mounted.splice(0).forEach((t) => t.destroy());
    mount();
    const heText = document.querySelector('.a11y-toolbar-root')?.textContent ?? '';
    for (const word of ['בודק נגישות', 'סורק', 'ציון', 'תקינות', 'שגיאות']) expect(heText).not.toContain(word);
  });

  it('gives every control an accessible name', () => {
    mount();
    for (const button of Array.from(panel().querySelectorAll('button'))) {
      const name = button.getAttribute('aria-label') ?? button.textContent ?? '';
      expect(name.trim().length, button.outerHTML).toBeGreaterThan(0);
    }
    for (const input of Array.from(panel().querySelectorAll('input'))) {
      expect(input.closest('label')?.textContent?.trim().length).toBeGreaterThan(0);
    }
  });
});

describe('controls', () => {
  it('toggles expose aria-pressed and apply the root attribute', () => {
    mount();
    for (const name of ['readableFont', 'pauseAnimations', 'reduceMotion', 'grayscale', 'highlightLinks', 'highlightHeadings',
      'readingGuide', 'readingMask', 'largeCursor', 'focusHighlight', 'hideImages']) {
      const button = control(name);
      expect(button.getAttribute('aria-pressed'), name).toBe('false');
      button.click();
      expect(button.getAttribute('aria-pressed'), name).toBe('true');
      const attr = `data-a11y-toolbar-${name.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`)}`;
      expect(html().hasAttribute(attr), attr).toBe(true);
      button.click();
      expect(html().hasAttribute(attr), attr).toBe(false);
    }
  });

  it('text size increases, decreases and resets', () => {
    mount();
    const value = document.getElementById(control('textScale-increase').getAttribute('aria-describedby') ?? '');
    expect(value?.textContent).toBe('100%');
    expect(control('textScale-decrease').getAttribute('aria-disabled')).toBe('true');
    control('textScale-increase').click();
    control('textScale-increase').click();
    expect(value?.textContent).toBe('120%');
    expect(html().getAttribute('data-a11y-toolbar-text-scale')).toBe('1.2');
    control('textScale-decrease').click();
    expect(html().getAttribute('data-a11y-toolbar-text-scale')).toBe('1.1');
    control('textScale-reset').click();
    expect(html().hasAttribute('data-a11y-toolbar-text-scale')).toBe(false);
    for (let i = 0; i < 10; i += 1) control('textScale-increase').click();
    expect(value?.textContent).toBe('160%');
    expect(control('textScale-increase').getAttribute('aria-disabled')).toBe('true');
  });

  it('letter spacing, word spacing and line height step through their values', () => {
    mount();
    control('letterSpacing-increase').click();
    control('wordSpacing-increase').click();
    control('wordSpacing-increase').click();
    control('lineHeight-increase').click();
    expect(html().getAttribute('data-a11y-toolbar-letter-spacing')).toBe('0.05');
    expect(html().getAttribute('data-a11y-toolbar-word-spacing')).toBe('0.2');
    expect(html().getAttribute('data-a11y-toolbar-line-height')).toBe('1.5');
    expect(html().style.getPropertyValue('--a11y-toolbar-word-spacing')).toBe('0.2em');
  });

  it('contrast modes are a mutually exclusive radio group', () => {
    mount();
    const radios = Array.from(panel().querySelectorAll<HTMLInputElement>('input[type="radio"]'));
    expect(radios).toHaveLength(5);
    expect(new Set(radios.map((r) => r.name)).size).toBe(1);
    expect(panel().querySelector('fieldset legend')?.textContent).toBe('מצב ניגודיות');
    const pick = (mode: string): void => {
      const input = control(`contrast-${mode}`) as HTMLInputElement;
      input.checked = true;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    };
    pick('highContrast');
    expect(html().hasAttribute('data-a11y-toolbar-high-contrast')).toBe(true);
    pick('darkContrast');
    expect(html().hasAttribute('data-a11y-toolbar-high-contrast')).toBe(false);
    expect(html().hasAttribute('data-a11y-toolbar-dark-contrast')).toBe(true);
    pick('lightContrast');
    expect(html().hasAttribute('data-a11y-toolbar-light-contrast')).toBe(true);
    pick('invertColors');
    expect(html().hasAttribute('data-a11y-toolbar-invert-colors')).toBe(true);
    expect(html().hasAttribute('data-a11y-toolbar-light-contrast')).toBe(false);
    pick('none');
    expect(radios.filter((r) => r.checked).map((r) => r.value)).toEqual(['none']);
    expect(html().hasAttribute('data-a11y-toolbar-invert-colors')).toBe(false);
  });

  it('announces changes once through a single polite live region', () => {
    vi.useFakeTimers();
    mount();
    const regions = document.querySelectorAll('.a11y-toolbar-root [aria-live]');
    expect(regions).toHaveLength(1);
    const live = regions[0];
    expect(live?.getAttribute('role')).toBe('status');
    expect(live?.getAttribute('aria-atomic')).toBe('true');
    control('textScale-increase').click();
    control('textScale-increase').click();
    vi.advanceTimersByTime(100);
    expect(live?.textContent).toBe('גודל הטקסט הוגדל ל־120 אחוזים');
    control('readableFont').click();
    vi.advanceTimersByTime(100);
    expect(live?.textContent).toBe('גופן קריא: פעיל');
    // No announcement when a value cannot change.
    control('letterSpacing-decrease').click();
    vi.advanceTimersByTime(100);
    expect(live?.textContent).toBe('גופן קריא: פעיל');
  });

  it('announces in English', () => {
    vi.useFakeTimers();
    mount({ language: 'en' });
    control('textScale-increase').click();
    control('textScale-increase').click();
    vi.advanceTimersByTime(100);
    expect(document.querySelector('.a11y-toolbar-root [role="status"]')?.textContent).toBe('Text size increased to 120 percent');
  });

  it('reset restores defaults, clears only its storage key, keeps the panel open and focuses the reset button', () => {
    vi.useFakeTimers();
    localStorage.setItem('unrelated', '1');
    const toolbar = mount();
    trigger().click();
    control('hideImages').click();
    control('textScale-increase').click();
    expect(localStorage.getItem(DEFAULT_STORAGE_KEY)).not.toBeNull();
    control('reset').click();
    expect(toolbar.provider.getPreferences()).toEqual(defaultPreferences);
    expect(localStorage.getItem(DEFAULT_STORAGE_KEY)).toBeNull();
    expect(localStorage.getItem('unrelated')).toBe('1');
    expect(Array.from(html().attributes).some((a) => a.name.startsWith('data-a11y-toolbar'))).toBe(false);
    expect(panel().hidden).toBe(false);
    expect(document.activeElement).toBe(control('reset'));
    vi.advanceTimersByTime(100);
    expect(document.querySelector('.a11y-toolbar-root [role="status"]')?.textContent).toBe('ההגדרות אופסו');
  });

  it('renders only enabled features', () => {
    mount({ enabledFeatures: ['readableFont', 'textScale'] });
    expect(document.querySelector('[data-a11y-toolbar-control="readableFont"]')).not.toBeNull();
    expect(document.querySelector('[data-a11y-toolbar-control="hideImages"]')).toBeNull();
    expect(document.querySelector('fieldset')).toBeNull();
  });

  it('applies translation overrides, panelTitle and buttonLabel', () => {
    mount({ language: 'en', translations: { resetAll: 'Start over' }, panelTitle: 'Display', buttonLabel: 'Display options' });
    expect(control('reset').textContent).toBe('Start over');
    expect(document.getElementById(panel().getAttribute('aria-labelledby') ?? '')?.textContent).toBe('Display');
    expect(trigger().getAttribute('aria-label')).toBe('Display options');
  });
});

describe('persistence and lifecycle', () => {
  it('restores saved preferences on mount', () => {
    localStorage.setItem(DEFAULT_STORAGE_KEY, JSON.stringify({ version: 1, preferences: { ...defaultPreferences, highlightLinks: true } }));
    mount();
    expect(control('highlightLinks').getAttribute('aria-pressed')).toBe('true');
    expect(html().hasAttribute('data-a11y-toolbar-highlight-links')).toBe(true);
  });

  it('survives corrupted storage', () => {
    localStorage.setItem(DEFAULT_STORAGE_KEY, '{"version":1,"preferences":{"textScale":"huge"');
    expect(() => mount()).not.toThrow();
    expect(trigger()).toBeTruthy();
  });

  it('applies preferences from another tab via the storage event', () => {
    vi.stubGlobal('BroadcastChannel', undefined);
    const toolbar = mount();
    expect(toolbar.provider.syncMode).toBe('storage');
    window.dispatchEvent(new StorageEvent('storage', {
      key: DEFAULT_STORAGE_KEY,
      newValue: JSON.stringify({ version: 1, preferences: { ...defaultPreferences, largeCursor: true } }),
    }));
    expect(control('largeCursor').getAttribute('aria-pressed')).toBe('true');
    vi.unstubAllGlobals();
  });

  it('calls onPreferenceChange and dispatches a namespaced event', () => {
    const onPreferenceChange = vi.fn();
    const listener = vi.fn();
    window.addEventListener('a11y-toolbar:preferences-change', listener);
    mount({ onPreferenceChange });
    control('focusHighlight').click();
    expect(onPreferenceChange).toHaveBeenCalledOnce();
    expect(listener).toHaveBeenCalledOnce();
    window.removeEventListener('a11y-toolbar:preferences-change', listener);
  });

  it('removes every side effect on destroy and remounts cleanly (Strict Mode style)', () => {
    const first = mount();
    control('readingGuide').click();
    control('textScale-increase').click();
    first.destroy();
    expect(document.querySelector('.a11y-toolbar-root')).toBeNull();
    expect(document.getElementById(RUNTIME_STYLE_ID)).toBeNull();
    expect(document.querySelector('[id^="a11y-toolbar"]')).toBeNull();
    expect(Array.from(html().attributes).some((a) => a.name.startsWith('data-a11y-toolbar'))).toBe(false);
    first.destroy();
    mount();
    expect(control('readingGuide').getAttribute('aria-pressed')).toBe('true');
    expect(document.getElementById('a11y-toolbar-reading-guide')).not.toBeNull();
    expect(document.querySelectorAll(`#${RUNTIME_STYLE_ID}`)).toHaveLength(1);
  });

  it('never renders a duplicate button and shares one stylesheet across instances', () => {
    const first = mount();
    const second = mount();
    expect(second.mounted).toBe(false);
    expect(document.querySelectorAll('#a11y-toolbar-trigger')).toHaveLength(1);
    expect(document.querySelectorAll(`#${RUNTIME_STYLE_ID}`)).toHaveLength(1);
    control('hideImages').click();
    second.destroy();
    expect(document.getElementById(RUNTIME_STYLE_ID)).not.toBeNull();
    expect(html().hasAttribute('data-a11y-toolbar-hide-images')).toBe(true);
    first.destroy();
    expect(document.getElementById(RUNTIME_STYLE_ID)).toBeNull();
    expect(html().hasAttribute('data-a11y-toolbar-hide-images')).toBe(false);
  });

  it('accepts a shared provider', () => {
    const provider = new AccessibilityProvider();
    const toolbar = AccessibilityToolbar({}, provider);
    provider.toggle('highlightHeadings');
    expect(control('highlightHeadings').getAttribute('aria-pressed')).toBe('true');
    toolbar.destroy();
    expect(html().hasAttribute('data-a11y-toolbar-highlight-headings')).toBe(true);
    provider.destroy();
    expect(html().hasAttribute('data-a11y-toolbar-highlight-headings')).toBe(false);
  });
});
