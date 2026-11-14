"use client";

import type { User } from "@supabase/supabase-js";
import { useEffect, useState } from "react";
import { getSupabase } from "./supabase/client";

/** undefined = עוד בודק, null = לא מחובר */
export function useUser() {
  const [user, setUser] = useState<User | null | undefined>(undefined);
  useEffect(() => {
    const sb = getSupabase();
    if (!sb) {
      setUser(null);
      return;
    }
    sb.auth.getUser().then(({ data }) => setUser(data.user ?? null));
    const { data } = sb.auth.onAuthStateChange((_e, s) => setUser(s?.user ?? null));
    return () => data.subscription.unsubscribe();
  }, []);
  return user;
}

export function loginHref(next: string) {
  return `/login?next=${encodeURIComponent(next)}`;
}
