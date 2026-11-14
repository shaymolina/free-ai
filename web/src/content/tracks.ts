export type Lesson = {
  slug: string;
  title: string;
  /** מזהה סרטון יוטיוב. ריק = השיעור עוד לא צולם */
  youtubeId?: string;
  minutes?: number;
  summary?: string;
  links?: { label: string; href: string }[];
  files?: { label: string; href: string }[];
  /** שיעור שבו צריך אחסון – מציג את קופסת 4CODE */
  hosting?: boolean;
};

export type Track = {
  slug: string;
  n: number;
  title: string;
  short: string;
  description: string;
  status: "open" | "soon";
  lessons: Lesson[];
};

export const tracks: Track[] = [
  {
    slug: "claude",
    n: 1,
    title: "Claude מאפס",
    short: "הקורס המלא. מהשאלה הראשונה ועד עבודה יומיומית.",
    description:
      "לומדים להשתמש ב-Claude כמו מקצוענים: איך מבקשים נכון, פרויקטים, קבצים, Artifacts, סקילים וחיבור לכלים – עם תרגול בכל שיעור.",
    status: "open",
    lessons: [
      { slug: "what-is-claude", title: "מה זה Claude ואיך מתחילים" },
      { slug: "asking-right", title: "איך מבקשים נכון" },
      { slug: "projects-and-files", title: "פרויקטים וקבצים" },
      { slug: "artifacts", title: "Artifacts – בונים דברים בתוך הצ'אט" },
      { slug: "skills", title: "סקילים – משדרגים את Claude בלחיצה" },
      { slug: "connectors", title: "חיבור לכלים שאתם כבר משתמשים בהם" },
      { slug: "claude-code", title: "Claude Code – בונים אתר בלי לכתוב קוד" },
      { slug: "going-live", title: "מעלים לאוויר", hosting: true },
    ],
  },
  {
    slug: "lovable",
    n: 2,
    title: "Lovable",
    short: "בונים אפליקציה אמיתית בלי לכתוב קוד.",
    description: "מרעיון לאפליקציה עובדת עם Lovable – מסכים, משתמשים, מסד נתונים ופרסום.",
    status: "soon",
    lessons: [],
  },
  {
    slug: "agents",
    n: 3,
    title: "סוכני AI",
    short: "עוזרים שעובדים בשבילכם, גם כשאתם לא.",
    description: "בונים סוכנים שעונים ללקוחות, מסכמים, מחפשים ומבצעים משימות לבד.",
    status: "soon",
    lessons: [],
  },
  {
    slug: "n8n",
    n: 4,
    title: "n8n",
    short: "אוטומציות שחוסכות שעות כל שבוע.",
    description: "מחברים בין כל הכלים בעסק ובונים תהליכים שרצים לבד, צעד אחרי צעד.",
    status: "soon",
    lessons: [],
  },
  {
    slug: "go-live",
    n: 5,
    title: "מעלים לאוויר",
    short: "אתר שעובד 24/7, צעד אחרי צעד.",
    description: "דומיין, אחסון ושרת שרץ כל הזמן – כל מה שצריך כדי שמה שבניתם יעבוד באמת.",
    status: "soon",
    lessons: [],
  },
];

export const getTrack = (slug: string) => tracks.find((t) => t.slug === slug);

export function getLesson(trackSlug: string, lessonSlug: string) {
  const track = getTrack(trackSlug);
  if (!track) return undefined;
  const i = track.lessons.findIndex((l) => l.slug === lessonSlug);
  if (i < 0) return undefined;
  return {
    track,
    lesson: track.lessons[i],
    index: i,
    prev: track.lessons[i - 1],
    next: track.lessons[i + 1],
  };
}
