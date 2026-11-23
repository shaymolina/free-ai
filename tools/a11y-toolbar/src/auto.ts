import { createAccessibilityToolbar } from './AccessibilityToolbar';
import { isToolbarLanguage } from './locales';
import type { AccessibilityToolbarProps, ToolbarPosition, ToolbarTheme } from './types';

/**
 * Drop-in build for plain HTML sites:
 * <script src="a11y-toolbar.js" data-language="he" data-position="bottom-right" async></script>
 * Configuration is read from data attributes only, as plain strings, and validated by the toolbar.
 */
function readConfig(script: HTMLOrSVGScriptElement | null): AccessibilityToolbarProps {
  const data = script instanceof HTMLScriptElement ? script.dataset : {};
  const z = Number(data.zIndex);
  const position = data.position as ToolbarPosition | undefined;
  const theme = data.theme as ToolbarTheme | undefined;
  return {
    language: isToolbarLanguage(data.language) ? data.language : 'he',
    ...(data.direction === 'rtl' || data.direction === 'ltr' ? { direction: data.direction } : {}),
    ...(position ? { position } : {}),
    ...(theme ? { theme } : {}),
    ...(data.primaryColor ? { primaryColor: data.primaryColor } : {}),
    ...(Number.isFinite(z) && data.zIndex ? { zIndex: z } : {}),
    ...(data.storageKey ? { storageKey: data.storageKey } : {}),
  };
}

if (typeof document !== 'undefined') {
  createAccessibilityToolbar(readConfig(document.currentScript));
}
