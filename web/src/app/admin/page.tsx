"use client";

import { useRouter } from "next/navigation";
import { Fragment, useEffect, useMemo, useState } from "react";
import { tracks } from "@/content/tracks";
import { getSupabase } from "@/lib/supabase/client";
import { useUser } from "@/lib/useUser";

type Profile = { id: string; email: string | null; full_name: string | null; created_at: string };
type Progress = { user_id: string; lesson_key: string; completed_at: string };
type Event = { user_id: string | null; type: string; target: string; created_at: string };

const day = (d: string) => d.slice(0, 10);
const fmt = (d: string) => new Date(d).toLocaleDateString("he-IL");

export default function Admin() {
  const user = useUser();
  const router = useRouter();
  const [ok, setOk] = useState<boolean | null>(null);
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [tab, setTab] = useState<"numbers" | "students" | "links">("numbers");
  const [openId, setOpenId] = useState<string | null>(null);

  useEffect(() => {
    if (user === null) router.replace("/login?next=/admin");
    const sb = getSupabase();
    if (!user || !sb) return;
    sb.from("profiles").select("is_admin").eq("id", user.id).maybeSingle().then(async ({ data }) => {
      if (!data?.is_admin) return setOk(false);
      setOk(true);
      const [p, pr, ev] = await Promise.all([
        sb.from("profiles").select("id,email,full_name,created_at").order("created_at", { ascending: false }).limit(5000),
        sb.from("progress").select("user_id,lesson_key,completed_at").limit(50000),
        sb.from("events").select("user_id,type,target,created_at").order("created_at", { ascending: false }).limit(50000),
      ]);
      setProfiles(p.data ?? []);
      setProgress(pr.data ?? []);
      setEvents(ev.data ?? []);
    });
  }, [user, router]);

  const byUser = useMemo(() => {
    const m = new Map<string, Progress[]>();
    progress.forEach((r) => m.set(r.user_id, [...(m.get(r.user_id) ?? []), r]));
    return m;
  }, [progress]);

  const name = (id: string | null) => {
    const p = profiles.find((x) => x.id === id);
    return p?.full_name || p?.email || "—";
  };

  const finishedTracks = (id: string) =>
    tracks.filter((t) => t.lessons.length && t.lessons.every((l) => (byUser.get(id) ?? []).some((r) => r.lesson_key === `${t.slug}/${l.slug}`)));

  const signupsByDay = useMemo(() => {
    const m = new Map<string, number>();
    profiles.forEach((p) => m.set(day(p.created_at), (m.get(day(p.created_at)) ?? 0) + 1));
    return [...m.entries()].sort().slice(-14);
  }, [profiles]);

  const links = useMemo(() => {
    const m = new Map<string, { type: string; n: number; users: Set<string> }>();
    events.filter((e) => e.type === "click" || e.type === "download").forEach((e) => {
      const x = m.get(e.target) ?? { type: e.type, n: 0, users: new Set<string>() };
      x.n++;
      if (e.user_id) x.users.add(e.user_id);
      m.set(e.target, x);
    });
    return [...m.entries()].sort((a, b) => b[1].n - a[1].n);
  }, [events]);

  if (ok === null) return <section className="page-hero" />;
  if (!ok)
    return (
      <section className="page-hero">
        <div className="container head"><h1 style={{ fontSize: 40 }}>אין גישה</h1></div>
      </section>
    );

  const week = Date.now() - 7 * 864e5;
  const max = Math.max(1, ...signupsByDay.map(([, n]) => n));
  const certs = profiles.reduce((s, p) => s + finishedTracks(p.id).length, 0);

  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <div className="container">
        <div className="head" style={{ marginBottom: 24 }}>
          <span className="tag">ניהול</span>
          <h1 style={{ fontSize: 48 }}>מסך ניהול</h1>
        </div>
        <div className="filters" role="tablist">
          {([["numbers", "מספרים"], ["students", "תלמידים"], ["links", "קישורים"]] as const).map(([k, l]) => (
            <button key={k} role="tab" aria-selected={tab === k} aria-pressed={tab === k} onClick={() => setTab(k)}>{l}</button>
          ))}
        </div>

        {tab === "numbers" && (
          <>
            <div className="stats" style={{ marginBottom: 20 }}>
              {[
                ["נרשמים", profiles.length],
                ["נרשמו השבוע", profiles.filter((p) => +new Date(p.created_at) > week).length],
                ["שיעורים שהושלמו", progress.length],
                ["מסלולים שהושלמו", certs],
                ["הורדות", events.filter((e) => e.type === "download").length],
                ["לחיצות על קישורים", events.filter((e) => e.type === "click").length],
              ].map(([l, n]) => (
                <div key={l} className="stat glass"><span className="num">{n}</span><span className="lbl">{l}</span></div>
              ))}
            </div>
            <div className="box glass">
              <h3>נרשמים לפי יום (14 ימים אחרונים)</h3>
              <div style={{ display: "flex", alignItems: "flex-end", gap: 6, height: 160, marginTop: 14 }}>
                {signupsByDay.map(([d, n]) => (
                  <div key={d} title={`${fmt(d)}: ${n}`} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                    <span style={{ fontSize: 12 }}>{n}</span>
                    <div style={{ width: "100%", height: `${(n / max) * 120}px`, background: "var(--ink)", borderRadius: 6 }} />
                    <span style={{ fontSize: 11, color: "var(--ink-3)" }}>{d.slice(8)}/{d.slice(5, 7)}</span>
                  </div>
                ))}
                {signupsByDay.length === 0 && <p>עוד אין נרשמים.</p>}
              </div>
            </div>
          </>
        )}

        {tab === "students" && (
          <div className="box glass" style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 15 }}>
              <thead>
                <tr style={{ textAlign: "start", color: "var(--ink-3)" }}>
                  <th style={{ textAlign: "start", padding: 8 }}>שם</th><th style={{ textAlign: "start", padding: 8 }}>מייל</th><th style={{ textAlign: "start", padding: 8 }}>נרשם</th><th style={{ textAlign: "start", padding: 8 }}>שיעורים</th><th style={{ textAlign: "start", padding: 8 }}>סיים</th>
                </tr>
              </thead>
              <tbody>
                {profiles.map((p) => (
                  <Fragment key={p.id}>
                    <tr onClick={() => setOpenId(openId === p.id ? null : p.id)} style={{ cursor: "pointer", borderTop: "1px solid var(--line)" }}>
                      <td style={{ padding: 8, fontWeight: 600 }}>{p.full_name || "—"}</td>
                      <td style={{ padding: 8 }} dir="ltr">{p.email}</td>
                      <td style={{ padding: 8 }}>{fmt(p.created_at)}</td>
                      <td style={{ padding: 8 }}>{byUser.get(p.id)?.length ?? 0}</td>
                      <td style={{ padding: 8 }}>{finishedTracks(p.id).map((t) => t.title).join(", ") || "—"}</td>
                    </tr>
                    {openId === p.id && (
                      <tr>
                        <td colSpan={5} style={{ padding: "8px 8px 18px", color: "var(--ink-2)" }}>
                          <b>שיעורים שהושלמו:</b> {(byUser.get(p.id) ?? []).map((r) => `${r.lesson_key} (${fmt(r.completed_at)})`).join(" · ") || "אין"}
                          <br />
                          <b>לחיצות והורדות:</b> {events.filter((e) => e.user_id === p.id && (e.type === "click" || e.type === "download")).map((e) => e.target).join(" · ") || "אין"}
                        </td>
                      </tr>
                    )}
                  </Fragment>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {tab === "links" && (
          <div className="box glass" style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 15 }}>
              <thead>
                <tr style={{ color: "var(--ink-3)" }}>
                  <th style={{ textAlign: "start", padding: 8 }}>קישור</th><th style={{ textAlign: "start", padding: 8 }}>סוג</th><th style={{ textAlign: "start", padding: 8 }}>לחיצות</th><th style={{ textAlign: "start", padding: 8 }}>מי לחץ</th>
                </tr>
              </thead>
              <tbody>
                {links.map(([href, x]) => (
                  <tr key={href} style={{ borderTop: "1px solid var(--line)" }}>
                    <td style={{ padding: 8, wordBreak: "break-all" }} dir="ltr">{href}</td>
                    <td style={{ padding: 8 }}>{x.type === "download" ? "הורדה" : "קישור"}</td>
                    <td style={{ padding: 8, fontWeight: 700 }}>{x.n}</td>
                    <td style={{ padding: 8 }}>{[...x.users].map(name).join(", ")}</td>
                  </tr>
                ))}
                {links.length === 0 && <tr><td style={{ padding: 8 }} colSpan={4}>עוד אין לחיצות.</td></tr>}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}
