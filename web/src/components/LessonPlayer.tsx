"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { IconPlay } from "./Icons";
import { getSupabase } from "@/lib/supabase/client";
import { loginHref, useUser } from "@/lib/useUser";
import { trackEvent } from "@/lib/track";

export default function LessonPlayer({ lessonKey, youtubeId, title }: { lessonKey: string; youtubeId?: string; title: string }) {
  const user = useUser();
  const path = usePathname();
  const [playing, setPlaying] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const sb = getSupabase();
    if (!user || !sb) return;
    localStorage.setItem("fa:last", path);
    sb.from("progress").select("lesson_key").eq("lesson_key", lessonKey).maybeSingle().then(({ data }) => setDone(!!data));
    trackEvent("view", lessonKey);
  }, [user, lessonKey, path]);

  async function toggleDone() {
    const sb = getSupabase();
    if (!sb || !user) return;
    if (done) {
      await sb.from("progress").delete().eq("user_id", user.id).eq("lesson_key", lessonKey);
      setDone(false);
    } else {
      await sb.from("progress").insert({ user_id: user.id, lesson_key: lessonKey });
      trackEvent("complete", lessonKey);
      setDone(true);
    }
  }

  return (
    <>
      <div className="player glass">
        {!youtubeId ? (
          <div className="video-frame">
            <span className="label">{title}</span>
            <span style={{ fontWeight: 600 }}>השיעור בצילום – יעלה בקרוב</span>
          </div>
        ) : playing && user ? (
          <iframe
            src={`https://www.youtube-nocookie.com/embed/${youtubeId}?autoplay=1&rel=0`}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : user ? (
          <button className="video-frame" onClick={() => setPlaying(true)} aria-label={`ניגון: ${title}`} style={{ backgroundImage: `linear-gradient(rgba(20,16,50,.35),rgba(20,16,50,.35)), url(https://i.ytimg.com/vi/${youtubeId}/hqdefault.jpg)`, backgroundSize: "cover", backgroundPosition: "center" }}>
            <span className="play"><IconPlay size={28} /></span>
          </button>
        ) : (
          <Link href={loginHref(path)} className="video-frame" aria-label="הרשמה כדי לצפות" style={{ backgroundImage: `linear-gradient(rgba(20,16,50,.45),rgba(20,16,50,.45)), url(https://i.ytimg.com/vi/${youtubeId}/hqdefault.jpg)`, backgroundSize: "cover", backgroundPosition: "center" }}>
            <span className="play"><IconPlay size={28} /></span>
            <span className="label" style={{ top: "auto", bottom: 16 }}>הרשמה חינם כדי לצפות</span>
          </Link>
        )}
      </div>
      {user && youtubeId && (
        <div style={{ marginTop: 16 }}>
          <button className={`btn ${done ? "btn-light" : "btn-dark"}`} onClick={toggleDone} aria-pressed={done}>
            {done ? "✓ סיימתי את השיעור" : "סיימתי שיעור"}
          </button>
        </div>
      )}
    </>
  );
}
