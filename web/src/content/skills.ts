export type Skill = {
  slug: string;
  title: string;
  category: string;
  meta: string;
  description: string;
  examplePrompt: string;
  exampleResult: string;
  source: string;
  download: string;
};

export const skillCategories = ["הכל", "אבטחה", "ביצועים", "כתיבה", "שיווק", "עסק", "קוד"];

export const skills: Skill[] = [
  {
    slug: "website-security",
    title: "בדיקת אבטחה לאתר ולאפליקציה",
    category: "אבטחה",
    meta: "34 בדיקות",
    description:
      "בודק 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI (Lovable, Bolt, Base44, Claude Code ועוד) ונותן דוח אדום / כתום / ירוק בעברית פשוטה.",
    examplePrompt: "תבדוק לי את האבטחה של האתר",
    exampleResult: "רשימה של כל החורים, מסודרת לפי מה לתקן קודם.",
    source: "https://github.com/openforge-lab/website-security",
    download: "https://github.com/openforge-lab/website-security/archive/refs/heads/main.zip",
  },
  {
    slug: "site-speed",
    title: "בדיקת מהירות לאתר",
    category: "ביצועים",
    meta: "69 בדיקות",
    description:
      "בודק 69 דברים שמאטים את האתר, כולל מיקום השרת מול הגולשים בישראל, ומדרג תיקונים לפי כמה שניות כל אחד חוסך – עם פרומפט מוכן לכל תיקון.",
    examplePrompt: "האתר שלי איטי, תבדוק",
    exampleResult: "דוח עם מה לתקן קודם ופרומפט מוכן להדבקה בכלי שבנה את האתר.",
    source: "https://github.com/openforge-lab/site-speed",
    download: "https://github.com/openforge-lab/site-speed/archive/refs/heads/main.zip",
  },
];

export const getSkill = (slug: string) => skills.find((s) => s.slug === slug);
