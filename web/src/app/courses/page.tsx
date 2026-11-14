import type { Metadata } from "next";
import Link from "next/link";
import Blobs from "@/components/Blobs";
import { IconArrow } from "@/components/Icons";
import { tracks } from "@/content/tracks";

export const metadata: Metadata = { title: "קורסים", description: "כל מסלולי הלימוד של Free AI – Claude, Lovable, סוכני AI, n8n והעלאה לאוויר. בחינם." };

export default function Courses() {
  return (
    <>
      <section className="page-hero">
        <Blobs preset="hero" />
        <div className="container" style={{ position: "relative" }}>
          <div className="head" data-reveal>
            <span className="tag">קורסים</span>
            <h1>כל המסלולים</h1>
            <p>מתחילים מאפס, מסיימים עם משהו שעובד. כל המסלולים בחינם.</p>
          </div>
        </div>
      </section>
      <section className="section" style={{ paddingTop: 20 }}>
        <div className="container">
          <div className="cards">
            {tracks.map((t, i) => (
              <Link key={t.slug} href={`/courses/${t.slug}`} className="card glass" data-reveal style={{ ["--d" as string]: `${i * 0.06}s`, minHeight: 240 }}>
                <span className="cat">מסלול {t.n}</span>
                <h3 style={{ fontSize: 26 }}>{t.title}</h3>
                <p>{t.short}</p>
                <span className="foot">
                  <span className="meta">{t.status === "open" ? `${t.lessons.length} שיעורים` : "בקרוב"}</span>
                  <IconArrow />
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
