import { describe, expect, it, vi } from 'vitest';
import {
  BOOLEAN_KEYS,
  CONTRAST_MODES,
  PREFERENCE_KEYS,
  PreferencesManager,
  STEPS,
  defaultPreferences,
  nextStep,
  sanitizePreferences,
} from '../../src/preferences';
import { createTranslations, en, he } from '../../src/locales';

describe('defaultPreferences', () => {
  it('has a typed default for every preference and is frozen', () => {
    expect(PREFERENCE_KEYS).toHaveLength(19);
    expect(Object.isFrozen(defaultPreferences)).toBe(true);
    expect(defaultPreferences.textScale).toBe(1);
    for (const key of BOOLEAN_KEYS) expect(defaultPreferences[key]).toBe(false);
  });

  it('has a localized label for every preference in both languages', () => {
    for (const key of PREFERENCE_KEYS) {
      expect(he[key]).toBeTruthy();
      expect(en[key]).toBeTruthy();
    }
  });
});

describe('sanitizePreferences', () => {
  it('returns defaults for non-objects', () => {
    expect(sanitizePreferences(null)).toEqual(defaultPreferences);
    expect(sanitizePreferences('x')).toEqual(defaultPreferences);
    expect(sanitizePreferences([1, 2])).toEqual(defaultPreferences);
  });

  it('keeps valid values, drops unknown fields and resets invalid ones', () => {
    const result = sanitizePreferences({
      textScale: 1.3, letterSpacing: 0.7, wordSpacing: 0.2, lineHeight: '2', readableFont: true,
      hideImages: 'yes', evil: '<script>',
    });
    expect(result.textScale).toBe(1.3);
    expect(result.letterSpacing).toBe(0);
    expect(result.wordSpacing).toBe(0.2);
    expect(result.lineHeight).toBe(0);
    expect(result.readableFont).toBe(true);
    expect(result.hideImages).toBe(false);
    expect('evil' in result).toBe(false);
  });

  it('rejects scales below the default and outside the list', () => {
    expect(sanitizePreferences({ textScale: 0.8 }).textScale).toBe(1);
    expect(sanitizePreferences({ textScale: 1.25 }).textScale).toBe(1);
    expect(sanitizePreferences({ textScale: 9 }).textScale).toBe(1);
  });

  it('keeps only one contrast mode, with deterministic precedence', () => {
    const result = sanitizePreferences({ invertColors: true, lightContrast: true, darkContrast: true });
    expect(result.darkContrast).toBe(true);
    expect(result.lightContrast).toBe(false);
    expect(result.invertColors).toBe(false);
  });
});

describe('nextStep', () => {
  it('moves through every step list and clamps at both ends', () => {
    expect(nextStep('textScale', 1, 1)).toBe(1.1);
    expect(nextStep('textScale', 1, -1)).toBe(1);
    expect(nextStep('textScale', 1.6, 1)).toBe(1.6);
    expect(nextStep('letterSpacing', 0.15, 1)).toBe(0.15);
    expect(nextStep('wordSpacing', 0.1, -1)).toBe(0);
    expect(nextStep('lineHeight', 0, 1)).toBe(1.5);
    expect(STEPS.textScale).toEqual([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]);
  });
});

describe('PreferencesManager', () => {
  it('updates immutably and notifies listeners with next and previous state', () => {
    const manager = new PreferencesManager();
    const listener = vi.fn();
    manager.subscribe(listener);
    const before = manager.get();
    manager.toggle('readableFont');
    const after = manager.get();
    expect(after).not.toBe(before);
    expect(before.readableFont).toBe(false);
    expect(after.readableFont).toBe(true);
    expect(Object.isFrozen(after)).toBe(true);
    expect(listener).toHaveBeenCalledWith(after, before);
  });

  it('does not notify when nothing changed', () => {
    const manager = new PreferencesManager();
    const listener = vi.fn();
    manager.subscribe(listener);
    manager.step('textScale', -1);
    manager.setPreference('readableFont', false);
    expect(listener).not.toHaveBeenCalled();
  });

  it('enforces contrast exclusivity for every mode', () => {
    const manager = new PreferencesManager();
    for (const mode of CONTRAST_MODES) {
      manager.setPreference(mode, true);
      for (const other of CONTRAST_MODES) expect(manager.get()[other]).toBe(other === mode);
    }
    manager.setContrastMode(null);
    for (const mode of CONTRAST_MODES) expect(manager.get()[mode]).toBe(false);
  });

  it('keeps grayscale independent from contrast modes', () => {
    const manager = new PreferencesManager();
    manager.toggle('grayscale');
    manager.setContrastMode('highContrast');
    expect(manager.get().grayscale).toBe(true);
    expect(manager.get().highContrast).toBe(true);
  });

  it('steps each stepped value', () => {
    const manager = new PreferencesManager();
    manager.step('textScale', 1);
    manager.step('letterSpacing', 1);
    manager.step('wordSpacing', 1);
    manager.step('lineHeight', 1);
    expect(manager.get()).toMatchObject({ textScale: 1.1, letterSpacing: 0.05, wordSpacing: 0.1, lineHeight: 1.5 });
  });

  it('ignores disabled features', () => {
    const manager = new PreferencesManager({ ...defaultPreferences, hideImages: true }, ['readableFont']);
    expect(manager.get().hideImages).toBe(false);
    manager.toggle('hideImages');
    expect(manager.get().hideImages).toBe(false);
    manager.toggle('readableFont');
    expect(manager.get().readableFont).toBe(true);
  });

  it('resets to defaults', () => {
    const manager = new PreferencesManager({ ...defaultPreferences, textScale: 1.5, readingMask: true });
    manager.reset();
    expect(manager.get()).toEqual(defaultPreferences);
  });

  it('keeps other listeners running when one throws', () => {
    const manager = new PreferencesManager();
    const good = vi.fn();
    manager.subscribe(() => {
      throw new Error('boom');
    });
    manager.subscribe(good);
    manager.toggle('largeCursor');
    expect(good).toHaveBeenCalledOnce();
  });
});

describe('createTranslations', () => {
  it('merges partial overrides and ignores empty strings', () => {
    const t = createTranslations('en', { resetAll: 'Start over', close: '' });
    expect(t.resetAll).toBe('Start over');
    expect(t.close).toBe(en.close);
    expect(t.panelTitle).toBe('Accessibility menu');
  });

  it('includes the required Hebrew strings', () => {
    const t = createTranslations('he');
    for (const text of [
      'אפשרויות נגישות', 'תפריט נגישות', 'סגירת תפריט הנגישות', 'הגדלת טקסט', 'הקטנת טקסט', 'גודל טקסט רגיל',
      'גופן קריא', 'ריווח אותיות', 'ריווח מילים', 'גובה שורה', 'עצירת אנימציות', 'הפחתת תנועה', 'גווני אפור',
      'ניגודיות גבוהה', 'ניגודיות כהה', 'ניגודיות בהירה', 'היפוך צבעים', 'הדגשת קישורים', 'הדגשת כותרות',
      'סרגל קריאה', 'מסכת קריאה', 'סמן עכבר גדול', 'הדגשת מיקוד', 'הסתרת תמונות', 'איפוס כל ההגדרות',
      'ההגדרות אופסו', 'פעיל', 'לא פעיל',
    ]) {
      expect(Object.values(t)).toContain(text);
    }
  });
});
