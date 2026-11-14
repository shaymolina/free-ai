import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Blobs from "@/components/Blobs";
import { IconArrow } from "@/components/Icons";
import { getTrack, tracks } from "@/content/tracks";
import ProgressMarks from "@/components/ProgressMarks";

export function generateStaticParams() {
  return tracks.map((t) => ({ track: t.slug }));
}

export async function generateMetadata({ params }: PageProps<"/courses/[track]">): Promise<Metadata> {
  const t = getTrack((await params).track);
  return t ? { title: t.title, description: t.description } : {};
}

export default async function TrackPage({ params }: PageProps<"/courses/[track]">) {
  const track = getTrack((await params).track);
  if (!track) notFound();
  const first = track.lessons[0];
  return (
    <>
      <section className="page-hero">
        <Blobs preset="hero" />
        <div className="container" style={{ position: "relative" }}>
          <div className="head" data-reveal>
            <nav className="crumbs" aria-label="פירורי לחם">
              <Link href="/courses">קורסים</Link> / <span>{track.title}</span>
            </nav>
            <span className="tag">מסלול {track.n}</span>
            <h1>{track.title}</h1>
            <p>{track.description}</p>
            {first && (
              <Link href={`/courses/${track.slug}/${first.slug}`} className="btn btn-dark" style={{ alignSelf: "flex-start" }}>
                מתחילים מהשיעור הראשון <IconArrow />
              </Link>
            )}
          </div>
        </div>
      </section>
      <section className="section" style={{ paddingTop: 20 }}>
        <div className="container">
          {track.lessons.length === 0 ? (
            <div className="box glass" data-reveal style={{ maxWidth: 820 }}>
              <h3>המסלול בהכנה</h3>
              <p>השיעורים יעלו בקרוב. בינתיים אפשר להתחיל עם <Link href="/courses/claude">Claude מאפס</Link>.</p>
            </div>
          ) : (
            <ol className="lessons" style={{ padding: 0, margin: 0 }}>
              {track.lessons.map((l, i) => (
                <li key={l.slug} style={{ listStyle: "none" }} data-reveal>
                  <Link href={`/courses/${track.slug}/${l.slug}`} className="lesson-row glass">
                    <span className="n" data-lesson={`${track.slug}/${l.slug}`}>{i + 1}</span>
                    <span className="title">{l.title}</span>
                    {!l.youtubeId && <span className="soon">בצילום</span>}
                    <IconArrow />
                  </Link>
                </li>
              ))}
            </ol>
          )}
          {track.lessons.length > 0 && (
            <ProgressMarks />
          )}
        </div>
      </section>
    </>
  );
}
