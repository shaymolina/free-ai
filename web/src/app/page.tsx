import Link from "next/link";
import Blobs from "@/components/Blobs";
import { IconArrow, IconAward, IconBolt, IconChat, IconCheck, IconFile, IconLink, IconPlay, IconPlus, IconServer, IconUser, IconVideo } from "@/components/Icons";
import { tracks } from "@/content/tracks";
import { skills } from "@/content/skills";

const tools = ["Claude", "Lovable", "n8n", "Claude Code", "ChatGPT", "Gemini", "Cursor", "Make", "Supabase", "Vercel"];

const faqs = [
  { q: "זה באמת בחינם?", a: "כן. כל השיעורים, הקבצים, הסקילים והתעודות – בחינם, בלי כרטיס אשראי ובלי מנוי." },
  { q: "למה צריך להירשם?", a: "ההרשמה שומרת לכם את ההתקדמות, פותחת את הסרטונים וההורדות, ומאפשרת לקבל תעודה בסוף מסלול. היא לוקחת פחות מדקה." },
  { q: "צריך ידע קודם?", a: "לא. כל מסלול מתחיל מאפס ומסביר כל צעד בעברית פשוטה." },
  { q: "יש תעודה?", a: "כן. מי שמסיים את כל השיעורים במסלול מקבל תעודת סיום עם השם שלו." },
  { q: "איך אתם מרוויחים אם הכל חינם?", a: "בשיעורים שבהם צריך אחסון אנחנו ממליצים על חברת אחסון שאנחנו עובדים איתה, ומקבלים עמלה אם נרשמים דרכנו. זה לא עולה לכם כלום." },
];

export default function Home() {
  const claude = tracks[0];
  return (
    <>
      {/* HERO */}
      <section className="hero">
        <Blobs preset="hero" />
        <div className="container hero-grid">
          <div>
            <span className="tag" data-reveal>
              100% בחינם · בעברית
            </span>
            <h1 data-reveal style={{ marginTop: 22, ["--d" as string]: ".08s" }}>
              הידע שעולה אלפים.
              <span className="thin">פתוח לכולם.</span>
            </h1>
            <p className="lead" data-reveal style={{ ["--d" as string]: ".16s" }}>
              Claude, Lovable, סוכני AI ואוטומציות n8n. שיעורים קצרים בעברית, מאפס ועד אתר שעובד באוויר.
            </p>
            <div className="actions" data-reveal style={{ ["--d" as string]: ".24s" }}>
              <Link href="/courses/claude" className="btn btn-dark">
                מתחילים ללמוד <IconArrow />
              </Link>
              <Link href="/skills" className="btn btn-light">
                ספריית הסקילים
              </Link>
            </div>
            <p className="free-note" data-reveal style={{ ["--d" as string]: ".3s" }}>
              בלי כרטיס אשראי. בלי מנוי. לתמיד.
            </p>
          </div>

          <div className="hero-visual" data-reveal style={{ ["--d" as string]: ".2s" }}>
            <Link href={`/courses/claude/${claude.lessons[0].slug}`} className="video-card glass" style={{ display: "block" }} aria-label="לשיעור הראשון">
              <div className="video-frame">
                <span className="label">שיעור 1 · {claude.lessons[0].title}</span>
                <span className="play">
                  <IconPlay size={28} />
                </span>
              </div>
            </Link>
            <div className="lesson-list-card glass">
              <h4>{claude.title}</h4>
              <ul>
                {claude.lessons.slice(0, 4).map((l, i) => (
                  <li key={l.slug} className={i === 2 ? "now" : ""}>
                    <span>{l.title.split(" – ")[0]}</span>
                    <span aria-hidden>{i < 2 ? "✓" : i === 2 ? "●" : "○"}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* TOOLS MARQUEE */}
      <div className="marquee" aria-label="הכלים שלומדים">
        <div className="marquee-track">
          {[...tools, ...tools].map((t, i) => (
            <span key={i} aria-hidden={i >= tools.length}>
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* TRACKS */}
      <section className="section" id="tracks">
        <Blobs preset="a" />
        <div className="container tracks-wrap">
          <div className="head" data-reveal>
            <span className="tag">המסלולים</span>
            <h2>מה לומדים כאן</h2>
            <p>חמישה מסלולים. מתחילים מאיפה שנוח לכם, ומסיימים עם משהו שעובד.</p>
            <Link href="/courses" className="btn btn-light" style={{ alignSelf: "flex-start" }}>
              לכל המסלולים <IconArrow />
            </Link>
          </div>
          <div className="track-list">
            {tracks.map((t, i) => (
              <details key={t.slug} className="track-item glass" open={i === 0} data-reveal style={{ ["--d" as string]: `${i * 0.06}s` }}>
                <summary>
                  <span className="t-title">
                    <span className="t-num">0{t.n}</span>
                    {t.title}
                  </span>
                  <span className="t-icon">
                    <IconPlus />
                  </span>
                </summary>
                <div className="t-body">
                  <p>{t.description}</p>
                  <div className="chips">
                    {t.status === "open" ? (
                      <>
                        <span className="chip">{t.lessons.length} שיעורים</span>
                        <span className="chip">תעודת סיום</span>
                        <span className="chip">קבצים להורדה</span>
                      </>
                    ) : (
                      <span className="chip">בקרוב</span>
                    )}
                  </div>
                  <Link href={`/courses/${t.slug}`} className="btn btn-light btn-sm">
                    {t.status === "open" ? "למסלול" : "פרטים"} <IconArrow />
                  </Link>
                </div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* PROCESS */}
      <section className="section">
        <Blobs preset="b" />
        <div className="container">
          <div className="head" data-reveal>
            <span className="tag">איך זה עובד</span>
            <h2>שלושה צעדים. אפס שקלים.</h2>
          </div>
          <div className="steps">
            {[
              { ico: <IconUser />, t: "נרשמים", d: "בלחיצה עם Google, או קוד למייל. בלי סיסמה." },
              { ico: <IconVideo />, t: "צופים ומתרגלים", d: "סרטון קצר, סיכום, וקבצים להורדה בכל שיעור." },
              { ico: <IconAward />, t: "מקבלים תעודה", d: "עם השם שלכם, בסוף כל מסלול." },
            ].map((s, i) => (
              <div key={s.t} className="step glass" data-reveal style={{ ["--d" as string]: `${i * 0.1}s` }}>
                <span className="ico">{s.ico}</span>
                <h3>{s.t}</h3>
                <p>{s.d}</p>
                <span className="count">
                  <b>0{i + 1}</b>/03
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES HUB */}
      <section className="section">
        <Blobs preset="c" />
        <div className="container">
          <div className="head center" data-reveal>
            <span className="tag">בכל שיעור</span>
            <h2>כל מה שצריך, במקום אחד</h2>
            <p>לא רק סרטון. כל שיעור בנוי כדי שתצאו ממנו עם משהו שעובד.</p>
          </div>
          <div className="hub">
            <div className="hub-col">
              {[
                { ico: <IconVideo />, t: "סרטון קצר וממוקד", d: "בלי חפירות. רק מה שצריך כדי להתקדם." },
                { ico: <IconFile />, t: "קבצים מוכנים", d: "תבניות n8n, פרומפטים וצ'קליסטים להורדה." },
                { ico: <IconCheck />, t: "שומר איפה עצרתם", d: "חוזרים ומגיעים ישר לשיעור הבא." },
              ].map((f, i) => (
                <div key={f.t} className="feature glass" data-reveal style={{ ["--d" as string]: `${i * 0.08}s` }}>
                  <span className="ico">{f.ico}</span>
                  <h3>{f.t}</h3>
                  <p>{f.d}</p>
                </div>
              ))}
            </div>
            <div className="hub-core" data-reveal>
              Free AI
            </div>
            <div className="hub-col">
              {[
                { ico: <IconLink />, t: "סיכום וקישורים", d: "כל מה שהוזכר בשיעור, מתחת לסרטון." },
                { ico: <IconServer />, t: "מעלים לאוויר", d: "הדרכה צעד-צעד לאחסון, כדי שזה ירוץ 24/7." },
                { ico: <IconChat />, t: "עזרה בוואטסאפ", d: "נתקעתם? שולחים שאלה בלחיצה." },
              ].map((f, i) => (
                <div key={f.t} className="feature glass" data-reveal style={{ ["--d" as string]: `${i * 0.08}s` }}>
                  <span className="ico">{f.ico}</span>
                  <h3>{f.t}</h3>
                  <p>{f.d}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* SKILLS */}
      <section className="section">
        <Blobs preset="a" />
        <div className="container split">
          <div className="head" data-reveal style={{ margin: 0 }}>
            <span className="tag">ספריית סקילים</span>
            <h2>משדרגים את Claude בלחיצה</h2>
            <p>ספריית סקילים בעברית שעושים עבודה אמיתית. מורידים, מתקינים, ומשתמשים.</p>
            <Link href="/skills" className="btn btn-light" style={{ alignSelf: "flex-start" }}>
              לכל הסקילים <IconArrow />
            </Link>
          </div>
          <div className="cards">
            {skills.map((s, i) => (
              <Link key={s.slug} href={`/skills/${s.slug}`} className="card glass" data-reveal style={{ ["--d" as string]: `${i * 0.1}s` }}>
                <span className="cat">{s.category}</span>
                <h3>{s.title}</h3>
                <span className="meta">{s.meta}</span>
                <span className="foot">
                  <span className="btn btn-dark btn-sm">הורדה חינם</span>
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* PRICING */}
      <section className="section">
        <Blobs preset="b" />
        <div className="container">
          <div className="head center" data-reveal>
            <span className="tag">מחיר</span>
            <h2>אותו ידע. בלי המחיר.</h2>
          </div>
          <div className="pricing">
            <div className="price glass old" data-reveal>
              <span className="p-name">קורס AI רגיל</span>
              <span className="p-amount">
                ₪3,000 <small>ומעלה</small>
              </span>
              <ul>
                <li>מחיר לכל קורס בנפרד</li>
                <li>גישה מוגבלת בזמן</li>
                <li>תבניות וקבצים בתשלום נוסף</li>
              </ul>
            </div>
            <div className="price glass best" data-reveal style={{ ["--d" as string]: ".1s" }}>
              <span className="p-name">Free AI</span>
              <span className="p-amount">
                ₪0 <small>לתמיד</small>
              </span>
              <ul>
                <li>כל המסלולים</li>
                <li>כל הקבצים והסקילים</li>
                <li>תעודת סיום לכל מסלול</li>
                <li>עזרה בוואטסאפ</li>
              </ul>
              <Link href="/login" className="btn btn-light">
                הרשמה חינם <IconArrow />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="section">
        <Blobs preset="c" />
        <div className="container">
          <div className="head center" data-reveal>
            <span className="tag">שאלות נפוצות</span>
            <h2>שאלות ותשובות</h2>
          </div>
          <div className="faq">
            {faqs.map((f, i) => (
              <details key={f.q} className="glass" data-reveal style={{ ["--d" as string]: `${i * 0.05}s` }}>
                <summary>{f.q}</summary>
                <p>{f.a}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section" style={{ paddingTop: 20 }}>
        <div className="container">
          <div className="cta glass" data-reveal>
            <Blobs preset="c" />
            <h2>מתחילים מהשיעור הראשון.</h2>
            <p>פחות מדקה להירשם. בחינם, לתמיד.</p>
            <Link href="/courses/claude" className="btn btn-dark">
              מתחילים ללמוד <IconBolt />
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
