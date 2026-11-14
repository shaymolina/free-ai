"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { getSupabase } from "@/lib/supabase/client";

export default function LoginForm() {
  const params = useSearchParams();
  const router = useRouter();
  const raw = params.get("next") ?? "/account";
  const next = raw.startsWith("/") && !raw.startsWith("//") ? raw : "/account";
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"email" | "code">("email");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(params.get("error") ? "הכניסה נכשלה. נסו שוב." : "");
  const sb = getSupabase();

  if (!sb) {
    return <p style={{ color: "var(--ink-2)" }}>ההרשמה תיפתח בקרוב.</p>;
  }

  async function google() {
    setBusy(true);
    const { error } = await sb!.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
    });
    if (error) {
      setMsg("הכניסה עם Google נכשלה. נסו שוב.");
      setBusy(false);
    }
  }

  async function sendCode(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMsg("");
    const { error } = await sb!.auth.signInWithOtp({ email: email.trim(), options: { shouldCreateUser: true } });
    setBusy(false);
    if (error) return setMsg("לא הצלחנו לשלוח קוד. בדקו את כתובת המייל.");
    setStep("code");
  }

  async function verify(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMsg("");
    const { error } = await sb!.auth.verifyOtp({ email: email.trim(), token: code.trim(), type: "email" });
    setBusy(false);
    if (error) return setMsg("הקוד לא נכון או שפג תוקפו.");
    router.replace(next);
    router.refresh();
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <button className="btn btn-dark" onClick={google} disabled={busy}>
        <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden>
          <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" />
          <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" />
          <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z" />
          <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z" />
        </svg>
        המשך עם Google
      </button>
      <div style={{ textAlign: "center", color: "var(--ink-3)", fontSize: 14 }}>או עם קוד למייל</div>
      {step === "email" ? (
        <form onSubmit={sendCode} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <input className="search" style={{ maxWidth: "none", margin: 0 }} type="email" required dir="ltr" placeholder="name@example.com" aria-label="כתובת מייל" value={email} onChange={(e) => setEmail(e.target.value)} />
          <button className="btn btn-light" disabled={busy}>שלחו לי קוד</button>
        </form>
      ) : (
        <form onSubmit={verify} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <p style={{ fontSize: 15, color: "var(--ink-2)" }}>שלחנו קוד ל-{email}</p>
          <input className="search" style={{ maxWidth: "none", margin: 0, letterSpacing: 6, textAlign: "center" }} inputMode="numeric" autoComplete="one-time-code" required dir="ltr" placeholder="••••••" aria-label="קוד מהמייל" value={code} onChange={(e) => setCode(e.target.value)} />
          <button className="btn btn-dark" disabled={busy}>כניסה</button>
          <button type="button" className="btn btn-light btn-sm" onClick={() => setStep("email")}>החלפת מייל</button>
        </form>
      )}
      {msg && <p role="alert" style={{ color: "#c0264b", fontSize: 15 }}>{msg}</p>}
      <p style={{ fontSize: 13, color: "var(--ink-3)" }}>בהרשמה אתם מסכימים ל<a href="/terms" style={{ textDecoration: "underline" }}>תנאי השימוש</a> ול<a href="/privacy" style={{ textDecoration: "underline" }}>מדיניות הפרטיות</a>.</p>
    </div>
  );
}
