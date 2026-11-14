import { getSupabase } from "./supabase/client";

/** רישום אירוע (צפייה / לחיצה / הורדה) */
export async function trackEvent(type: "view" | "complete" | "click" | "download", target: string) {
  const sb = getSupabase();
  if (!sb) return;
  const { data } = await sb.auth.getUser();
  if (!data.user) return;
  await sb.from("events").insert({ user_id: data.user.id, type, target });
}
