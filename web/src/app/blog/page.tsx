import type { Metadata } from "next";
import Link from "next/link";
import Blobs from "@/components/Blobs";
import { posts } from "@/content/posts";

export const metadata: Metadata = { title: "בלוג מדריכים", description: "מדריכים פתוחים בעברית על Claude, סקילים, Lovable, סוכני AI ו-n8n." };

const fmt = (d: string) => new Date(d).toLocaleDateString("he-IL", { day: "numeric", month: "long", year: "numeric" });

export default function Blog() {
  return (
    <>
      <section className="page-hero">
        <Blobs preset="hero" />
        <div className="container" style={{ position: "relative" }}>
          <div className="head" data-reveal>
            <span className="tag">בלוג</span>
            <h1>מדריכים פתוחים</h1>
            <p>קוראים בלי להירשם. כשרוצים להעמיק – יש קורס.</p>
          </div>
        </div>
      </section>
      <section className="section" style={{ paddingTop: 20 }}>
        <div className="container cards">
          {posts.map((p) => (
            <Link key={p.slug} href={`/blog/${p.slug}`} className="card glass" data-reveal>
              <span className="cat">{fmt(p.date)} · {p.minutes} דקות קריאה</span>
              <h3>{p.title}</h3>
              <p>{p.excerpt}</p>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
