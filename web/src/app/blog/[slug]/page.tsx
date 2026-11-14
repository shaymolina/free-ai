import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Blobs from "@/components/Blobs";
import { IconArrow } from "@/components/Icons";
import { getPost, posts } from "@/content/posts";
import { site } from "@/content/site";

export function generateStaticParams() {
  return posts.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: PageProps<"/blog/[slug]">): Promise<Metadata> {
  const p = getPost((await params).slug);
  return p ? { title: p.title, description: p.excerpt, openGraph: { type: "article" } } : {};
}

export default async function PostPage({ params }: PageProps<"/blog/[slug]">) {
  const p = getPost((await params).slug);
  if (!p) notFound();
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: p.title,
    description: p.excerpt,
    datePublished: p.date,
    inLanguage: "he",
    publisher: { "@type": "Organization", name: site.name, url: site.url },
  };
  return (
    <article className="page-hero" style={{ paddingBottom: 100 }}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }} />
      <Blobs preset="a" />
      <div className="container" style={{ position: "relative" }}>
        <div className="head" data-reveal style={{ maxWidth: 760 }}>
          <nav className="crumbs" aria-label="פירורי לחם">
            <Link href="/blog">בלוג</Link>
          </nav>
          <h1 style={{ fontSize: "clamp(34px,5vw,58px)" }}>{p.title}</h1>
          <p>{p.excerpt}</p>
        </div>
        <div className="prose">
          {p.body.map((b, i) => (b.startsWith("## ") ? <h2 key={i}>{b.slice(3)}</h2> : <p key={i}>{b}</p>))}
        </div>
        <div className="cta glass" style={{ marginTop: 60, maxWidth: 760, padding: "48px 28px" }}>
          <h2 style={{ fontSize: 34 }}>רוצים ללמוד את זה לעומק?</h2>
          <p>כל הקורסים בחינם. פחות מדקה להירשם.</p>
          <Link href="/login" className="btn btn-dark">
            הרשמה חינם <IconArrow />
          </Link>
        </div>
      </div>
    </article>
  );
}
