"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getTrack } from "@/content/tracks";
import { getSupabase } from "@/lib/supabase/client";
import { useUser } from "@/lib/useUser";
import { trackEvent } from "@/lib/track";

export default function Certificate() {
  const { track: slug } = useParams<{ track: string }>();
  const track = getTrack(slug);
  const user = useUser();
  const router = useRouter();
  const [state, setState] = useState<{ ok: boolean; name: string; date: string } | null>(null);

  useEffect(() => {
    if (user === null) router.replace(`/login?next=/certificate/${slug}`);
    const sb = getSupabase();
    if (!user || !sb || !track) return;
    Promise.all([
      sb.from("progress").select("lesson_key,completed_at").like("lesson_key", `${slug}/%`),
      sb.from("profiles").select("full_name").eq("id", user.id).maybeSingle(),
    ]).then(([p, prof]) => {
      const rows = p.data ?? [];
      const keys = new Set(rows.map((r) => r.lesson_key));
      const ok = track.lessons.length > 0 && track.lessons.every((l) => keys.has(`${slug}/${l.slug}`));
      const lastDate = rows.map((r) => r.completed_at).sort().pop() ?? new Date().toISOString();
      setState({ ok, name: prof.data?.full_name || user.email || "", date: new Date(lastDate).toLocaleDateString("he-IL", { day: "numeric", month: "long", year: "numeric" }) });
      if (ok) trackEvent("view", `certificate:${slug}`);
    });
  }, [user, slug, track, router]);

  if (!track) return null;
  if (!state) return <section className="page-hero" />;
  if (!state.ok)
    return (
      <section className="page-hero">
        <div className="container head">
          <h1 style={{ fontSize: 40 }}>עוד לא סיימתם את המסלול</h1>
          <p>התעודה נפתחת אחרי שכל השיעורים ב{track.title} מסומנים כהושלמו.</p>
        </div>
      </section>
    );

  return (
    <section className="page-hero cert-page">
      <style>{`
        .cert { max-width: 1000px; margin: 0 auto; aspect-ratio: 1.414; padding: 6%; display: flex; flex-direction: column; justify-content: space-between; text-align: center; position: relative; overflow: hidden;
          background: radial-gradient(60% 60% at 0% 0%, rgba(125,155,255,.35), transparent), radial-gradient(60% 60% at 100% 100%, rgba(255,159,214,.35), transparent), radial-gradient(50% 50% at 100% 0%, rgba(181,140,255,.3), transparent), #fff;
          border-radius: 28px; border: 1px solid var(--line); box-shadow: var(--shadow); }
        .cert h1 { font-size: clamp(28px, 5vw, 56px); }
        .cert .who { font-size: clamp(30px, 6vw, 68px); font-weight: 900; letter-spacing: -.03em; }
        @media print {
          @page { size: A4 landscape; margin: 0; }
          .site-header, .site-footer, .wa, .no-print { display: none !important; }
          .cert-page { padding: 0 !important; }
          .cert { box-shadow: none; border: 0; border-radius: 0; width: 100vw; max-width: none; height: 100vh; aspect-ratio: auto; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        }
      `}</style>
      <div className="container">
        <div className="cert">
          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 10, fontWeight: 800, fontSize: 22 }}>
            <span className="logo-mark" /> Free AI
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <p style={{ color: "var(--ink-3)", fontSize: 18 }}>תעודת סיום</p>
            <div className="who">{state.name}</div>
            <p style={{ fontSize: 20, color: "var(--ink-2)" }}>סיים/ה בהצלחה את המסלול</p>
            <h1>{track.title}</h1>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", color: "var(--ink-3)", fontSize: 15 }}>
            <span>{state.date}</span>
            <span>free-ai.co.il</span>
          </div>
        </div>
        <div className="no-print" style={{ display: "flex", gap: 10, justifyContent: "center", marginTop: 24 }}>
          <button className="btn btn-dark" onClick={() => window.print()}>
            הורדה כ-PDF
          </button>
        </div>
      </div>
    </section>
  );
}
