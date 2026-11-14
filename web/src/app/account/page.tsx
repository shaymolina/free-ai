"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Blobs from "@/components/Blobs";
import { IconArrow } from "@/components/Icons";
import { tracks } from "@/content/tracks";
import { getSupabase } from "@/lib/supabase/client";
import { useUser } from "@/lib/useUser";

export default function Account() {
  const user = useUser();
  const router = useRouter();
  const [done, setDone] = useState<Set<string>>(new Set());
  const [name, setName] = useState("");
  const [saved, setSaved] = useState(false);
  const [admin, setAdmin] = useState(false);
  const [last, setLast] = useState<string | null>(null);

  useEffect(() => {
    if (user === null) router.replace("/login?next=/account");
    const sb = getSupabase();
    if (!user || !sb) return;
    setLast(localStorage.getItem("fa:last"));
    sb.from("progress").select("lesson_key").then(({ data }) => setDone(new Set((data ?? []).map((r) => r.lesson_key))));
    sb.from("profiles").select("full_name,is_admin").eq("id", user.id).maybeSingle().then(({ data }) => {
      setName(data?.full_name ?? "");
      setAdmin(!!data?.is_admin);
    });
  }, [user, router]);

  if (!user) return <section className="page-hero" />;

  async function saveName(e: React.FormEvent) {
    e.preventDefault();
    await getSupabase()!.from("profiles").update({ full_name: name.trim() }).eq("id", user!.id);
    setSaved(true);
  }

  async function logout() {
    await getSupabase()!.auth.signOut();
    router.replace("/");
  }

  const open = tracks.filter((t) => t.lessons.length > 0);
  const nextOf = (t: (typeof tracks)[number]) => t.lessons.find((l) => !done.has(`${t.slug}/${l.slug}`));

  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <Blobs preset="hero" />
      <div className="container" style={{ position: "relative" }}>
        <div className="head">
          <span className="tag">האזור שלי</span>
          <h1 style={{ fontSize: "clamp(36px,5vw,60px)" }}>שלום{name ? `, ${name}` : ""}</h1>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {last && (
              <Link href={last} className="btn btn-dark">
                המשך מאיפה שעצרתי <IconArrow />
              </Link>
            )}
            {admin && (
              <Link href="/admin" className="btn btn-light">
                מסך ניהול
              </Link>
            )}
            <button className="btn btn-light" onClick={logout}>
              יציאה
            </button>
          </div>
        </div>

        <div className="cards" style={{ marginBottom: 28 }}>
          {open.map((t) => {
            const n = t.lessons.filter((l) => done.has(`${t.slug}/${l.slug}`)).length;
            const complete = n === t.lessons.length;
            const nx = nextOf(t);
            return (
              <div key={t.slug} className="card glass">
                <span className="cat">מסלול {t.n}</span>
                <h3>{t.title}</h3>
                <div style={{ height: 8, borderRadius: 8, background: "rgba(15,15,40,.08)", overflow: "hidden" }}>
                  <div style={{ width: `${(n / t.lessons.length) * 100}%`, height: "100%", background: "var(--ink)" }} />
                </div>
                <span className="meta">
                  {n} מתוך {t.lessons.length} שיעורים
                </span>
                <span className="foot">
                  {complete ? (
                    <Link href={`/certificate/${t.slug}`} className="btn btn-dark btn-sm">
                      לתעודה שלי
                    </Link>
                  ) : (
                    <Link href={`/courses/${t.slug}/${nx!.slug}`} className="btn btn-dark btn-sm">
                      לשיעור הבא
                    </Link>
                  )}
                </span>
              </div>
            );
          })}
        </div>

        <form className="box glass" onSubmit={saveName} style={{ maxWidth: 520, display: "flex", flexDirection: "column", gap: 10 }}>
          <h3>השם שיופיע בתעודה</h3>
          <input className="search" style={{ maxWidth: "none", margin: 0 }} value={name} onChange={(e) => { setName(e.target.value); setSaved(false); }} placeholder="שם מלא" aria-label="שם מלא" required />
          <button className="btn btn-light btn-sm" style={{ alignSelf: "flex-start" }}>{saved ? "✓ נשמר" : "שמירה"}</button>
        </form>
      </div>
    </section>
  );
}
