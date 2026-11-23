import type { ToolbarTranslations } from '../types';
import { el } from './dom';
import { AccessibilityIcon, createIcon } from './icons';

export const PANEL_ID = 'a11y-panel';
export const TRIGGER_ID = 'a11y-toolbar-trigger';

export function FloatingAccessibilityButton(doc: Document, label: string, className: string): HTMLButtonElement {
  return el(doc, 'button', {
    className,
    id: TRIGGER_ID,
    attrs: {
      type: 'button',
      'aria-expanded': 'false',
      'aria-controls': PANEL_ID,
      'aria-haspopup': 'dialog',
      'aria-label': label,
      title: label,
    },
  }, [AccessibilityIcon(doc)]);
}

export interface PanelParts {
  readonly panel: HTMLDivElement;
  readonly title: HTMLHeadingElement;
  readonly close: HTMLButtonElement;
  readonly body: HTMLDivElement;
  readonly footer: HTMLDivElement;
}

/** Non-modal dialog shell: the page stays usable, so there is no focus trap and aria-modal is false. */
export function AccessibilityPanel(doc: Document, t: ToolbarTranslations, title: string, className: string, uid: string): PanelParts {
  const titleId = `a11y-toolbar-${uid}-title`;
  const descId = `a11y-toolbar-${uid}-desc`;
  const heading = el(doc, 'h2', { className: 'a11y-toolbar-title', id: titleId, text: title, attrs: { tabindex: '-1' } });
  const close = el(doc, 'button', {
    className: 'a11y-toolbar-close a11y-toolbar-nav',
    attrs: { type: 'button', 'aria-label': t.close, title: t.close, 'data-a11y-toolbar-control': 'close' },
  }, [createIcon(doc, 'close')]);
  const body = el(doc, 'div', { className: 'a11y-toolbar-body' });
  const footer = el(doc, 'div', { className: 'a11y-toolbar-footer' });
  const panel = el(doc, 'div', {
    className,
    id: PANEL_ID,
    attrs: { role: 'dialog', 'aria-modal': 'false', 'aria-labelledby': titleId, 'aria-describedby': descId },
  }, [
    el(doc, 'div', { className: 'a11y-toolbar-header' }, [
      el(doc, 'div', { className: 'a11y-toolbar-heading' }, [
        el(doc, 'span', { className: 'a11y-toolbar-heading-icon', attrs: { 'aria-hidden': 'true' } }, [AccessibilityIcon(doc, 'a11y-toolbar-icon')]),
        heading,
      ]),
      close,
    ]),
    el(doc, 'p', { className: 'a11y-toolbar-description', id: descId, text: t.panelDescription }),
    body,
    footer,
  ]);
  panel.hidden = true;
  return { panel, title: heading, close, body, footer };
}

/** The toolbar's one polite live region. Identical consecutive messages are re-announced only when triggered again by the user. */
export class LiveAnnouncer {
  readonly element: HTMLDivElement;
  private timer: ReturnType<typeof setTimeout> | null = null;

  constructor(doc: Document) {
    this.element = el(doc, 'div', {
      className: 'a11y-toolbar-sr-only',
      attrs: { role: 'status', 'aria-live': 'polite', 'aria-atomic': 'true' },
    });
  }

  announce(message: string): void {
    if (this.timer !== null) clearTimeout(this.timer);
    this.element.textContent = '';
    this.timer = setTimeout(() => {
      this.timer = null;
      this.element.textContent = message;
    }, 60);
  }

  destroy(): void {
    if (this.timer !== null) clearTimeout(this.timer);
    this.timer = null;
  }
}
