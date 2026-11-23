import { headOrRoot } from '../utils/browser';

export const TEXT_SCALE_STYLE_ID = 'a11y-toolbar-text-scale-styles';
export const SCALE_VAR = '--a11y-toolbar-text-scale';

/** Elements that never receive scaled text. */
const EXCLUDED = [
  '.a11y-toolbar-root', '.a11y-toolbar-root *', '[data-a11y-toolbar-overlay]', '[data-a11y-toolbar-overlay] *',
  '[data-a11y-toolbar-ignore-text-scale]', '[data-a11y-toolbar-ignore-text-scale] *',
  'svg', 'svg *', 'canvas', 'iframe', 'embed', 'object',
  '.cm-editor', '.cm-editor *', '.CodeMirror', '.CodeMirror *', '.monaco-editor', '.monaco-editor *',
].join(', ');

/** Splits a selector list on top-level commas only. */
export function splitSelectors(selectorText: string): string[] {
  const out: string[] = [];
  let depth = 0;
  let quote: string | null = null;
  let current = '';
  for (const ch of selectorText) {
    if (quote) {
      if (ch === quote) quote = null;
    } else if (ch === '"' || ch === "'") {
      quote = ch;
    } else if (ch === '(' || ch === '[') {
      depth += 1;
    } else if (ch === ')' || ch === ']') {
      depth -= 1;
    } else if (ch === ',' && depth === 0) {
      out.push(current.trim());
      current = '';
      continue;
    }
    current += ch;
  }
  if (current.trim()) out.push(current.trim());
  return out;
}

/** Adds the exclusion to a single selector, keeping pseudo-elements last. */
export function scopeSelector(selector: string): string {
  const pseudo = /::?(?:before|after|first-line|first-letter|marker|placeholder|selection)\b.*$/i.exec(selector);
  if (pseudo) {
    const base = selector.slice(0, pseudo.index);
    return `${base || '*'}:not(${EXCLUDED})${pseudo[0]}`;
  }
  return `${selector}:not(${EXCLUDED})`;
}

/**
 * Only absolute or viewport-based sizes need an override. Relative sizes (em, %, rem) already
 * follow the scaled root or parent, so overriding them would scale twice.
 */
export function isScalableFontSize(value: string): boolean {
  const v = value.trim().toLowerCase();
  if (!v || v.includes('rem')) return false;
  return /\d(?:px|pt|vw|vh|vmin|vmax|cm|mm|in|pc)\b/.test(v) || v.startsWith('var(');
}

interface RuleLike {
  readonly type: number;
  readonly cssRules?: CSSRuleList;
}

function isStyleRule(rule: CSSRule): rule is CSSStyleRule {
  return 'selectorText' in rule && 'style' in rule;
}

function collect(rules: CSSRuleList, out: string[]): void {
  for (const rule of Array.from(rules)) {
    if (isStyleRule(rule)) {
      const size = rule.style.getPropertyValue('font-size');
      if (size && isScalableFontSize(size)) {
        const selectors = splitSelectors(rule.selectorText).map(scopeSelector).join(', ');
        out.push(`${selectors}{font-size:calc(${size} * var(${SCALE_VAR})) !important}`);
      }
      continue;
    }
    if ('media' in rule && 'cssRules' in rule && !('styleSheet' in rule)) {
      const media = rule as CSSMediaRule;
      const inner: string[] = [];
      collect(media.cssRules, inner);
      if (inner.length) out.push(`@media ${media.media.mediaText}{${inner.join('')}}`);
      continue;
    }
    if ('containerQuery' in rule && 'conditionText' in rule && 'cssRules' in rule) {
      const container = rule as CSSContainerRule;
      const inner: string[] = [];
      collect(container.cssRules, inner);
      if (inner.length) out.push(`@container ${container.containerName} ${container.containerQuery}{${inner.join('')}}`);
      continue;
    }
    if ('conditionText' in rule && 'cssRules' in rule) {
      const supports = rule as CSSSupportsRule;
      const inner: string[] = [];
      collect(supports.cssRules, inner);
      if (inner.length) out.push(`@supports ${supports.conditionText}{${inner.join('')}}`);
      continue;
    }
    if ('styleSheet' in rule) {
      const imported = (rule as CSSImportRule).styleSheet;
      const nested = imported ? readRules(imported) : null;
      if (nested) collect(nested, out);
      continue;
    }
    const maybe = rule as RuleLike;
    if (maybe.cssRules && !('name' in rule)) collect(maybe.cssRules, out);
  }
}

function readRules(sheet: CSSStyleSheet): CSSRuleList | null {
  try {
    return sheet.cssRules;
  } catch {
    // Cross-origin sheets cannot be read; they are skipped.
    return null;
  }
}

/** Builds override rules that scale every absolute font-size declared by the host's same-origin stylesheets. */
export function buildTextScaleCss(doc: Document): string {
  const out: string[] = [`html:not([data-a11y-toolbar-ignore-text-scale]){font-size:calc(100% * var(${SCALE_VAR})) !important}`];
  const own = new Set(Array.from(doc.querySelectorAll<HTMLStyleElement>('style[id^="a11y-toolbar"]')).map((el) => el.sheet));
  for (const sheet of Array.from(doc.styleSheets)) {
    if (own.has(sheet)) continue;
    if (sheet.disabled) continue;
    const rules = readRules(sheet);
    if (rules) collect(rules, out);
  }
  return out.join('\n');
}

/** Keeps the generated text-scale sheet in sync with the selected scale. */
export class TypographyManager {
  private style: HTMLElement | null = null;
  private stopLoad: () => void = () => undefined;

  constructor(private readonly doc: Document) {}

  update(scale: number): void {
    if (scale === 1) {
      this.remove();
      return;
    }
    if (!this.style) {
      this.refresh();
      const win = this.doc.defaultView;
      if (win && this.doc.readyState !== 'complete') {
        const onLoad = (): void => this.refresh();
        win.addEventListener('load', onLoad, { once: true });
        this.stopLoad = () => win.removeEventListener('load', onLoad);
      }
    }
  }

  /** Rebuilds the generated rules, for example after the host added stylesheets. */
  refresh(): void {
    let css = '';
    try {
      css = buildTextScaleCss(this.doc);
    } catch {
      return;
    }
    const existing = this.doc.getElementById(TEXT_SCALE_STYLE_ID);
    const style = existing && existing.tagName === 'STYLE' ? existing : this.doc.createElement('style');
    style.id = TEXT_SCALE_STYLE_ID;
    style.textContent = css;
    if (!style.isConnected) headOrRoot(this.doc).appendChild(style);
    this.style = style;
  }

  remove(): void {
    this.stopLoad();
    this.stopLoad = () => undefined;
    this.style?.remove();
    this.doc.getElementById(TEXT_SCALE_STYLE_ID)?.remove();
    this.style = null;
  }
}
