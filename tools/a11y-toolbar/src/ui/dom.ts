type Child = Node | string | null | undefined | false;

export interface ElementProps {
  readonly className?: string;
  readonly id?: string;
  readonly text?: string;
  readonly attrs?: Readonly<Record<string, string>>;
}

/** Tiny element factory. Text goes through textContent, never through HTML parsing. */
export function el<K extends keyof HTMLElementTagNameMap>(
  doc: Document,
  tag: K,
  props: ElementProps = {},
  children: readonly Child[] = [],
): HTMLElementTagNameMap[K] {
  const node = doc.createElement(tag);
  if (props.className) node.className = props.className;
  if (props.id) node.id = props.id;
  if (props.text !== undefined) node.textContent = props.text;
  if (props.attrs) for (const [name, value] of Object.entries(props.attrs)) node.setAttribute(name, value);
  for (const child of children) {
    if (child === null || child === undefined || child === false) continue;
    node.appendChild(typeof child === 'string' ? doc.createTextNode(child) : child);
  }
  return node;
}

export function joinClasses(...names: readonly (string | undefined)[]): string {
  return names
    .flatMap((name) => (name ?? '').split(/\s+/))
    .filter((name) => /^[\w-]+$/.test(name))
    .join(' ');
}
