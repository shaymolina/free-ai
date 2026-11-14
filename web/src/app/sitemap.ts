import type { MetadataRoute } from "next";
import { site } from "@/content/site";
import { tracks } from "@/content/tracks";
import { skills } from "@/content/skills";
import { posts } from "@/content/posts";

export default function sitemap(): MetadataRoute.Sitemap {
  const u = (p: string) => `${site.url}${p}`;
  return [
    ...["", "/courses", "/skills", "/blog", "/about", "/privacy", "/terms"].map((p) => ({ url: u(p) })),
    ...tracks.map((t) => ({ url: u(`/courses/${t.slug}`) })),
    ...tracks.flatMap((t) => t.lessons.map((l) => ({ url: u(`/courses/${t.slug}/${l.slug}`) }))),
    ...skills.map((s) => ({ url: u(`/skills/${s.slug}`) })),
    ...posts.map((p) => ({ url: u(`/blog/${p.slug}`), lastModified: p.date })),
  ];
}
