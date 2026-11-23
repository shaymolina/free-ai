import type { ResolvedReadingGuideOptions, ResolvedReadingMaskOptions } from '../types';
import { cancelFrame, requestFrame } from '../utils/browser';

export const GUIDE_ID = 'a11y-toolbar-reading-guide';
export const MASK_TOP_ID = 'a11y-toolbar-reading-mask-top';
export const MASK_BOTTOM_ID = 'a11y-toolbar-reading-mask-bottom';

function overlay(doc: Document, id: string, className: string): HTMLDivElement {
  const el = doc.createElement('div');
  el.id = id;
  el.className = className;
  el.setAttribute('aria-hidden', 'true');
  el.setAttribute('data-a11y-toolbar-overlay', '');
  return el;
}

/**
 * Shared pointer and focus tracking for the reading guide and the reading mask.
 * Listeners exist only while at least one of the tools is on, and updates run once per animation frame.
 */
abstract class PointerFollower {
  protected y: number | null = null;
  private frame = 0;
  private listening = false;
  protected readonly win: Window | null;

  constructor(protected readonly doc: Document, protected readonly host: HTMLElement, private readonly followFocus: boolean) {
    this.win = doc.defaultView;
  }

  private readonly onPointer = (event: PointerEvent | MouseEvent): void => {
    if (event.clientY === this.y) return;
    this.y = event.clientY;
    this.schedule();
  };

  private readonly onFocus = (event: FocusEvent): void => {
    const target = event.target;
    if (!(target instanceof Element) || this.host.contains(target) || target.closest('.a11y-toolbar-root')) return;
    const rect = target.getBoundingClientRect();
    this.focusRect = rect;
    this.y = rect.top + rect.height / 2;
    this.schedule();
  };

  protected focusRect: DOMRect | null = null;

  protected schedule(): void {
    if (this.frame) return;
    this.frame = requestFrame(this.win, () => {
      this.frame = 0;
      this.render();
    });
  }

  protected listen(on: boolean): void {
    const win = this.win;
    if (!win || on === this.listening) return;
    this.listening = on;
    if (on) {
      win.addEventListener('pointermove', this.onPointer, { passive: true });
      if (this.followFocus) this.doc.addEventListener('focusin', this.onFocus);
    } else {
      win.removeEventListener('pointermove', this.onPointer);
      this.doc.removeEventListener('focusin', this.onFocus);
      cancelFrame(win, this.frame);
      this.frame = 0;
    }
  }

  protected viewportHeight(): number {
    return this.win?.innerHeight ?? 0;
  }

  protected abstract render(): void;
}

export class ReadingGuideManager extends PointerFollower {
  private el: HTMLDivElement | null = null;

  constructor(doc: Document, host: HTMLElement, private readonly options: ResolvedReadingGuideOptions) {
    super(doc, host, options.followFocus);
  }

  update(active: boolean): void {
    if (active === (this.el !== null)) return;
    if (active) {
      const el = overlay(this.doc, GUIDE_ID, 'a11y-toolbar-reading-guide');
      el.style.setProperty('--a11y-toolbar-guide-color', this.options.color);
      el.style.setProperty('--a11y-toolbar-guide-thickness', `${this.options.thickness}px`);
      this.host.appendChild(el);
      this.el = el;
      this.y = this.y ?? this.viewportHeight() / 2;
      this.render();
      this.listen(true);
    } else {
      this.destroy();
    }
  }

  protected render(): void {
    if (!this.el || this.y === null) return;
    const top = Math.round(this.y - this.options.thickness / 2);
    this.el.style.transform = `translate3d(0, ${top}px, 0)`;
  }

  destroy(): void {
    this.listen(false);
    this.el?.remove();
    this.el = null;
  }
}

export class ReadingMaskManager extends PointerFollower {
  private top: HTMLDivElement | null = null;
  private bottom: HTMLDivElement | null = null;

  constructor(doc: Document, host: HTMLElement, private readonly options: ResolvedReadingMaskOptions) {
    super(doc, host, options.followFocus);
  }

  update(active: boolean): void {
    if (active === (this.top !== null)) return;
    if (active) {
      this.top = overlay(this.doc, MASK_TOP_ID, 'a11y-toolbar-reading-mask a11y-toolbar-reading-mask-top');
      this.bottom = overlay(this.doc, MASK_BOTTOM_ID, 'a11y-toolbar-reading-mask a11y-toolbar-reading-mask-bottom');
      for (const el of [this.top, this.bottom]) {
        el.style.setProperty('--a11y-toolbar-mask-opacity', String(this.options.opacity));
        this.host.appendChild(el);
      }
      this.y = this.y ?? this.viewportHeight() / 2;
      this.render();
      this.listen(true);
    } else {
      this.destroy();
    }
  }

  protected render(): void {
    if (!this.top || !this.bottom || this.y === null) return;
    const vh = this.viewportHeight();
    // The clear band always covers the focused element, even when it is taller than the configured area.
    const focusHeight = this.focusRect ? this.focusRect.height + 16 : 0;
    this.focusRect = null;
    const half = Math.max(this.options.areaHeight, focusHeight) / 2;
    const start = Math.max(0, Math.round(this.y - half));
    const end = Math.min(vh, Math.round(this.y + half));
    this.top.style.height = `${start}px`;
    this.bottom.style.top = `${end}px`;
  }

  destroy(): void {
    this.listen(false);
    this.top?.remove();
    this.bottom?.remove();
    this.top = null;
    this.bottom = null;
  }
}
