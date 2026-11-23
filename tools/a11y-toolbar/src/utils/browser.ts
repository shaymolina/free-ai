/** Feature detection helpers. Every function is safe to call during server-side rendering. */

export function getDocument(doc?: Document): Document | null {
  if (doc) return doc;
  return typeof document === 'undefined' ? null : document;
}

export function getWindow(doc: Document | null): (Window & typeof globalThis) | null {
  const view = doc?.defaultView;
  return view ?? null;
}

export function safeMatchMedia(win: Window | null, query: string): MediaQueryList | null {
  if (!win || typeof win.matchMedia !== 'function') return null;
  try {
    return win.matchMedia(query);
  } catch {
    return null;
  }
}

export function listenMedia(list: MediaQueryList | null, handler: () => void): () => void {
  if (!list) return () => undefined;
  if (typeof list.addEventListener === 'function') {
    list.addEventListener('change', handler);
    return () => list.removeEventListener('change', handler);
  }
  return () => undefined;
}

export function requestFrame(win: Window | null, cb: () => void): number {
  if (win && typeof win.requestAnimationFrame === 'function') return win.requestAnimationFrame(cb);
  cb();
  return 0;
}

export function cancelFrame(win: Window | null, id: number): void {
  if (id && win && typeof win.cancelAnimationFrame === 'function') win.cancelAnimationFrame(id);
}

export function createId(): string {
  const cryptoObj = typeof globalThis.crypto === 'object' ? globalThis.crypto : undefined;
  if (cryptoObj && typeof cryptoObj.randomUUID === 'function') return cryptoObj.randomUUID();
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

/** Accepts hex, rgb(a) and hsl(a) colors only, so configuration can never inject CSS. */
export function isSafeColor(value: unknown): value is string {
  if (typeof value !== 'string') return false;
  const v = value.trim();
  return /^#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$/i.test(v)
    || /^(?:rgb|hsl)a?\(\s*[\d.%\s,/+-]+\)$/i.test(v);
}

export function clampNumber(value: unknown, min: number, max: number, fallback: number): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) return fallback;
  return Math.min(max, Math.max(min, value));
}

/** document.body and document.head are typed as always present, but are null while a script in <head> runs. */
export function bodyOf(doc: Document): HTMLElement | null {
  return doc.body as HTMLElement | null;
}

export function headOrRoot(doc: Document): HTMLElement {
  return (doc.head as HTMLHeadElement | null) ?? doc.documentElement;
}
