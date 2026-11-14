const base = { width: 22, height: 22, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };

export const IconPlay = ({ size = 24 }: { size?: number }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
    <path d="M7 4.5v15a1 1 0 0 0 1.5.9l12-7.5a1 1 0 0 0 0-1.8l-12-7.5A1 1 0 0 0 7 4.5z" />
  </svg>
);
export const IconUser = () => (<svg {...base}><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></svg>);
export const IconVideo = () => (<svg {...base}><rect x="3" y="5" width="14" height="14" rx="3" /><path d="M17 10l4-2v8l-4-2" /></svg>);
export const IconAward = () => (<svg {...base}><circle cx="12" cy="9" r="6" /><path d="M8.5 14l-1.5 7 5-3 5 3-1.5-7" /></svg>);
export const IconFile = () => (<svg {...base}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" /><path d="M14 3v5h5M9 13h6M9 17h6" /></svg>);
export const IconLink = () => (<svg {...base}><path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1" /><path d="M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1" /></svg>);
export const IconCheck = () => (<svg {...base}><path d="M5 12l5 5 9-10" /></svg>);
export const IconBolt = () => (<svg {...base}><path d="M13 2L4 14h7l-1 8 9-12h-7z" /></svg>);
export const IconServer = () => (<svg {...base}><rect x="3" y="4" width="18" height="7" rx="2" /><rect x="3" y="13" width="18" height="7" rx="2" /><path d="M7 7.5h.01M7 16.5h.01" /></svg>);
export const IconChat = () => (<svg {...base}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" /></svg>);
export const IconPlus = () => (<svg {...base} width={16} height={16}><path d="M12 5v14M5 12h14" /></svg>);
export const IconArrow = () => (<span className="arrow" aria-hidden>←</span>);
