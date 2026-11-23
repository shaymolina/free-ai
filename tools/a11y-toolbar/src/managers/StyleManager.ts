import { headOrRoot } from '../utils/browser';

export const RUNTIME_STYLE_ID = 'a11y-toolbar-runtime-styles';
const REFS = 'a11yToolbarRefs';

/**
 * Injects the toolbar's single runtime stylesheet once per document.
 * The reference count lives on the element itself, so several mounted toolbars share one sheet
 * and the last one to unmount removes it.
 */
export function acquireRuntimeStyles(doc: Document, css: string): () => void {
  let released = false;
  let el: HTMLElement | null = doc.getElementById(RUNTIME_STYLE_ID);
  try {
    if (!el || el.tagName !== 'STYLE') {
      const style = doc.createElement('style');
      style.id = RUNTIME_STYLE_ID;
      style.textContent = css;
      headOrRoot(doc).appendChild(style);
      el = style;
    }
    el.dataset[REFS] = String(Number(el.dataset[REFS] ?? '0') + 1);
  } catch {
    el = null;
  }
  return () => {
    if (released || !el) return;
    released = true;
    const refs = Number(el.dataset[REFS] ?? '1') - 1;
    if (refs <= 0) el.remove();
    else el.dataset[REFS] = String(refs);
  };
}

export function runtimeStyleRefs(doc: Document): number {
  const el = doc.getElementById(RUNTIME_STYLE_ID);
  return el ? Number(el.dataset[REFS] ?? '0') : 0;
}
