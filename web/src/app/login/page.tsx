import type { Metadata } from "next";
import { Suspense } from "react";
import Blobs from "@/components/Blobs";
import LoginForm from "./LoginForm";

export const metadata: Metadata = { title: "הרשמה וכניסה", robots: { index: false } };

export default function Login() {
  return (
    <section className="page-hero" style={{ paddingBottom: 100, minHeight: "90vh" }}>
      <Blobs preset="hero" />
      <div className="container" style={{ position: "relative", display: "grid", placeItems: "center" }}>
        <div className="glass" style={{ width: "100%", maxWidth: 440, padding: 32 }} data-reveal>
          <span className="tag">חינם, לתמיד</span>
          <h1 style={{ fontSize: 34, margin: "14px 0 8px" }}>הרשמה או כניסה</h1>
          <p style={{ color: "var(--ink-2)", marginBottom: 24 }}>פחות מדקה. בלי סיסמה.</p>
          <Suspense>
            <LoginForm />
          </Suspense>
        </div>
      </div>
    </section>
  );
}
