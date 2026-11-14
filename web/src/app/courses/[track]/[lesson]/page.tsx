import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Blobs from "@/components/Blobs";
import LessonPlayer from "@/components/LessonPlayer";
import { getLesson, tracks } from "@/content/tracks";
import { site } from "@/content/site";
import TrackedLink from "@/components/TrackedLink";

export function generateStaticParams() {
  return tracks.flatMap((t) => t.lessons.map((l) => ({ track: t.slug, lesson: l.slug })));
}

export async function generateMetadata({ params }: PageProps<"/courses/[track]/[lesson]">): Promise<Metadata> {
  const { track, lesson } = await params;
  const r = getLesson(track, lesson);
  return r ? { title: `${r.lesson.title} – ${r.track.title}`, description: r.lesson.summary ?? r.track.description } : {};
}

export default async function LessonPage({ params }: PageProps<"/courses/[track]/[lesson]">) {
  const p = await params;
  const r = getLesson(p.track, p.lesson);
  if (!r) notFound();
  const { track, lesson, index, prev, next } = r;
  const base = `/courses/${track.slug}`;
  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <Blobs preset="a" />
      <div className="container" style={{ position: "relative" }}>
        <nav className="crumbs" aria-label="פירורי לחם" style={{ marginBottom: 14 }}>
          <Link href="/courses">קורסים</Link> / <Link href={base}>{track.title}</Link> / <span>שיעור {index + 1}</span>
        </nav>
        <h1 style={{ fontSize: "clamp(30px,4vw,48px)", marginBottom: 28 }}>{lesson.title}</h1>
        <div className="lesson-layout">
          <div>
            <LessonPlayer lessonKey={`${track.slug}/${lesson.slug}`} youtubeId={lesson.youtubeId} title={lesson.title} />
            <div className="lesson-body">
              {lesson.summary && (
                <div className="box glass">
                  <h3>סיכום</h3>
                  <p>{lesson.summary}</p>
                </div>
              )}
              {lesson.links && lesson.links.length > 0 && (
                <div className="box glass">
                  <h3>קישורים מהשיעור</h3>
                  <ul>
                    {lesson.links.map((l) => (
                      <li key={l.href}>
                        <TrackedLink href={l.href}>{l.label}</TrackedLink>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {lesson.files && lesson.files.length > 0 && (
                <div className="box glass">
                  <h3>קבצים להורדה</h3>
                  <ul>
                    {lesson.files.map((f) => (
                      <li key={f.href}>
                        <TrackedLink href={f.href} kind="download">{f.label}</TrackedLink>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {lesson.hosting && (
                <div className="box glass hosting">
                  <h3>איפה מעלים לאוויר?</h3>
                  <p>כדי שמה שבניתם ירוץ 24/7 צריך אחסון. אנחנו עובדים עם {site.hostingName} – בעברית, עם תמיכה בארץ.</p>
                  <p style={{ marginTop: 14 }}>
                    <TrackedLink className="btn btn-dark btn-sm" href={site.hostingUrl} sponsored>
                      ל-{site.hostingName}
                    </TrackedLink>
                  </p>
                  <p className="disclosure">גילוי נאות: אנחנו מקבלים עמלה על הרשמה דרך הקישור, בלי עלות נוספת לכם.</p>
                </div>
              )}
              <div className="pager">
                {prev ? <Link className="btn btn-light" href={`${base}/${prev.slug}`}>→ הקודם</Link> : <span />}
                {next ? <Link className="btn btn-dark" href={`${base}/${next.slug}`}>הבא ←</Link> : <Link className="btn btn-dark" href={base}>סיום המסלול</Link>}
              </div>
            </div>
          </div>
          <aside className="glass" aria-label="שיעורי המסלול">
            <h4>{track.title}</h4>
            {track.lessons.map((l, i) => (
              <Link key={l.slug} href={`${base}/${l.slug}`} aria-current={l.slug === lesson.slug ? "page" : undefined}>
                {i + 1}. {l.title}
              </Link>
            ))}
          </aside>
        </div>
      </div>
    </section>
  );
}
