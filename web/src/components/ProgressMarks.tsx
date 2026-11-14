"use client";

import { useEffect } from "react";
import { getSupabase } from "@/lib/supabase/client";
import { useUser } from "@/lib/useUser";

/** מסמן ✓ ליד שיעורים שהושלמו (אלמנטים עם data-lesson) */
export default function ProgressMarks() {
  const user = useUser();
  useEffect(() => {
    const sb = getSupabase();
    if (!user || !sb) return;
    sb.from("progress").select("lesson_key").then(({ data }) => {
      const done = new Set((data ?? []).map((r) => r.lesson_key));
      document.querySelectorAll<HTMLElement>("[data-lesson]").forEach((el) => {
        if (done.has(el.dataset.lesson!)) {
          el.classList.add("done");
          el.textContent = "✓";
        }
      });
    });
  }, [user]);
  return null;
}
