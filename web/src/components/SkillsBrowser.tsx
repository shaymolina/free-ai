"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { skillCategories, skills } from "@/content/skills";

export default function SkillsBrowser() {
  const [cat, setCat] = useState("הכל");
  const [q, setQ] = useState("");
  const list = useMemo(
    () =>
      skills.filter(
        (s) => (cat === "הכל" || s.category === cat) && (!q || (s.title + s.description + s.category).includes(q.trim())),
      ),
    [cat, q],
  );
  const cats = skillCategories.filter((c) => c === "הכל" || skills.some((s) => s.category === c));
  return (
    <>
      <input className="search" type="search" placeholder="חיפוש סקיל…" aria-label="חיפוש סקיל" value={q} onChange={(e) => setQ(e.target.value)} />
      <div className="filters" role="group" aria-label="קטגוריות">
        {cats.map((c) => (
          <button key={c} aria-pressed={cat === c} onClick={() => setCat(c)}>
            {c}
          </button>
        ))}
      </div>
      <div className="cards">
        {list.map((s) => (
          <Link key={s.slug} href={`/skills/${s.slug}`} className="card glass">
            <span className="cat">{s.category}</span>
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <span className="foot">
              <span className="meta">{s.meta}</span>
              <span className="btn btn-dark btn-sm">הורדה חינם</span>
            </span>
          </Link>
        ))}
        {list.length === 0 && <p>לא נמצאו סקילים. נסו מילה אחרת.</p>}
      </div>
    </>
  );
}
