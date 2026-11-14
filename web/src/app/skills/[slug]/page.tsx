import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Blobs from "@/components/Blobs";
import TrackedLink from "@/components/TrackedLink";
import { getSkill, skills } from "@/content/skills";
import { posts } from "@/content/posts";

export function generateStaticParams() {
  return skills.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: PageProps<"/skills/[slug]">): Promise<Metadata> {
  const s = getSkill((await params).slug);
  return s ? { title: s.title, description: s.description } : {};
}

export default async function SkillPage({ params }: PageProps<"/skills/[slug]">) {
  const s = getSkill((await params).slug);
  if (!s) notFound();
  const howTo = posts.find((p) => p.slug === "how-to-install-claude-skill");
  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <Blobs preset="hero" />
      <div className="container" style={{ position: "relative" }}>
        <div className="head" data-reveal style={{ marginBottom: 36 }}>
          <nav className="crumbs" aria-label="פירורי לחם">
            <Link href="/skills">סקילים</Link> / <span>{s.category}</span>
          </nav>
          <h1 style={{ fontSize: "clamp(34px,5vw,60px)" }}>{s.title}</h1>
          <p>{s.description}</p>
        </div>
        <div className="skill-detail">
          <div className="box glass example" data-reveal>
            <h3>דוגמה לשימוש</h3>
            <div className="bubble me">{s.examplePrompt}</div>
            <div className="bubble">{s.exampleResult}</div>
          </div>
          <div className="box glass" data-reveal style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <span className="tag" style={{ alignSelf: "flex-start" }}>{s.meta}</span>
            <TrackedLink href={s.download} kind="download" className="btn btn-dark">
              הורדה חינם
            </TrackedLink>
            {howTo && (
              <Link href={`/blog/${howTo.slug}`} className="btn btn-light">
                איך מתקינים סקיל?
              </Link>
            )}
            <TrackedLink href={s.source} className="meta">
              קוד המקור
            </TrackedLink>
          </div>
        </div>
      </div>
    </section>
  );
}
