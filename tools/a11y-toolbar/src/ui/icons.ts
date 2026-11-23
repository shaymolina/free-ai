const SVG_NS = 'http://www.w3.org/2000/svg';

type Shape =
  | { readonly tag: 'path'; readonly d: string }
  | { readonly tag: 'circle'; readonly cx: number; readonly cy: number; readonly r: number }
  | { readonly tag: 'rect'; readonly x: number; readonly y: number; readonly width: number; readonly height: number; readonly rx: number };

const p = (d: string): Shape => ({ tag: 'path', d });

/** Lucide "Accessibility" (wheelchair) glyph, exact shapes. */
const ACCESSIBILITY: readonly Shape[] = [
  { tag: 'circle', cx: 16, cy: 4, r: 1 },
  p('m18 19 1-7-6 1'),
  p('m5 8 3-3 5.5 3-2.36 3.5'),
  p('M4.24 14.5a5 5 0 0 0 6.88 6'),
  p('M13.76 17.5a5 5 0 0 0-6.88-6'),
];

export const ICONS = {
  accessibility: ACCESSIBILITY,
  close: [p('M18 6 6 18'), p('m6 6 12 12')],
  check: [p('M20 6 9 17l-5-5')],
  minus: [p('M5 12h14')],
  plus: [p('M5 12h14'), p('M12 5v14')],
  reset: [p('M3 12a9 9 0 1 0 3-6.7L3 8'), p('M3 3v5h5')],
  font: [p('M4 20 10 4h1l6 16'), p('M6.5 14h8'), p('M19 20v-6'), p('M16 17h6')],
  spacing: [p('M3 12h18'), p('m6 9-3 3 3 3'), p('m18 9 3 3-3 3')],
  lineHeight: [p('M10 6h11'), p('M10 12h11'), p('M10 18h11'), p('m3 8 3-3 3 3'), p('m3 16 3 3 3-3'), p('M6 5v14')],
  text: [p('M4 7V5h16v2'), p('M12 5v14'), p('M9 19h6')],
  pause: [{ tag: 'rect', x: 6, y: 5, width: 4, height: 14, rx: 1 }, { tag: 'rect', x: 14, y: 5, width: 4, height: 14, rx: 1 }],
  motion: [p('M3 12h4l3-8 4 16 3-8h4')],
  grayscale: [{ tag: 'circle', cx: 12, cy: 12, r: 9 }, p('M12 3a9 9 0 0 1 0 18Z')],
  link: [p('M10 14a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.5 1.5'), p('M14 10a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.5-1.5')],
  heading: [p('M6 4v16'), p('M18 4v16'), p('M6 12h12')],
  guide: [p('M3 12h18'), p('M3 6h10'), p('M3 18h14')],
  mask: [{ tag: 'rect', x: 3, y: 3, width: 18, height: 18, rx: 2 }, p('M3 9h18'), p('M3 15h18')],
  cursor: [p('M5 3l14 7-6 2-2 6Z')],
  focus: [p('M3 8V5a2 2 0 0 1 2-2h3'), p('M16 3h3a2 2 0 0 1 2 2v3'), p('M21 16v3a2 2 0 0 1-2 2h-3'), p('M8 21H5a2 2 0 0 1-2-2v-3'), { tag: 'circle', cx: 12, cy: 12, r: 3 }],
  image: [{ tag: 'rect', x: 3, y: 3, width: 18, height: 18, rx: 2 }, { tag: 'circle', cx: 9, cy: 9, r: 2 }, p('m21 15-5-5L5 21'), p('M3 3l18 18')],
} as const satisfies Readonly<Record<string, readonly Shape[]>>;

export type IconName = keyof typeof ICONS;

/** Builds an inline SVG with DOM APIs only. Icons are decorative: hidden from assistive technology. */
export function createIcon(doc: Document, name: IconName, className = 'a11y-toolbar-icon'): SVGSVGElement {
  const svg = doc.createElementNS(SVG_NS, 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('fill', 'none');
  svg.setAttribute('stroke', 'currentColor');
  svg.setAttribute('stroke-width', '2');
  svg.setAttribute('stroke-linecap', 'round');
  svg.setAttribute('stroke-linejoin', 'round');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  svg.setAttribute('class', className);
  for (const shape of ICONS[name] as readonly Shape[]) {
    const el = doc.createElementNS(SVG_NS, shape.tag);
    if (shape.tag === 'path') el.setAttribute('d', shape.d);
    else if (shape.tag === 'circle') {
      el.setAttribute('cx', String(shape.cx));
      el.setAttribute('cy', String(shape.cy));
      el.setAttribute('r', String(shape.r));
    } else {
      el.setAttribute('x', String(shape.x));
      el.setAttribute('y', String(shape.y));
      el.setAttribute('width', String(shape.width));
      el.setAttribute('height', String(shape.height));
      el.setAttribute('rx', String(shape.rx));
    }
    svg.appendChild(el);
  }
  return svg;
}

/** The floating button's wheelchair icon. */
export function AccessibilityIcon(doc: Document, className = 'a11y-toolbar-trigger-icon'): SVGSVGElement {
  return createIcon(doc, 'accessibility', className);
}
