// @vitest-environment node
import { describe, expect, it } from 'vitest';
import { AccessibilityProvider, createAccessibilityToolbar, defaultPreferences } from '../../src';

describe('server-side rendering safety', () => {
  it('has no document, window or storage in this environment', () => {
    expect(typeof document).toBe('undefined');
    expect(typeof window).toBe('undefined');
  });

  it('creates a toolbar without touching browser APIs', () => {
    const toolbar = createAccessibilityToolbar({ language: 'en' });
    expect(toolbar.mounted).toBe(false);
    expect(toolbar.isOpen()).toBe(false);
    expect(() => {
      toolbar.open();
      toolbar.destroy();
    }).not.toThrow();
  });

  it('keeps provider state in memory', () => {
    const provider = new AccessibilityProvider();
    expect(provider.isBrowser).toBe(false);
    expect(provider.syncMode).toBe('none');
    provider.toggle('readableFont');
    expect(provider.getPreferences().readableFont).toBe(true);
    provider.reset();
    expect(provider.getPreferences()).toEqual(defaultPreferences);
    provider.destroy();
  });
});
