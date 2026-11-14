"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { nav } from "@/content/site";
import { useUser } from "@/lib/useUser";

export function Logo() {
  return (
    <Link href="/" className="logo" aria-label="Free AI – דף הבית">
      <span className="logo-mark" aria-hidden />
      Free AI
    </Link>
  );
}

export default function Header() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const user = useUser();
  const isCurrent = (href: string) => (path === href || path.startsWith(href + "/") ? "page" : undefined);

  return (
    <header className="site-header">
      <div className="bar glass">
        <Logo />
        <nav className="site-nav" aria-label="ניווט ראשי">
          {nav.map((n) => (
            <Link key={n.href} href={n.href} aria-current={isCurrent(n.href)}>
              {n.label}
            </Link>
          ))}
        </nav>
        <div className="header-actions">
          {user ? (
            <Link href="/account" className="btn btn-dark btn-sm">
              האזור שלי
            </Link>
          ) : (
            <>
              <Link href="/login" className="login">
                כניסה
              </Link>
              <Link href="/login" className="btn btn-dark btn-sm">
                הרשמה חינם
              </Link>
            </>
          )}
          <button
            className="menu-btn"
            aria-label={open ? "סגירת תפריט" : "פתיחת תפריט"}
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
            </svg>
          </button>
        </div>
      </div>
      <div className={`mobile-menu glass ${open ? "open" : ""}`}>
        {nav.map((n) => (
          <Link key={n.href} href={n.href} onClick={() => setOpen(false)}>
            {n.label}
          </Link>
        ))}
        {user ? (
          <Link href="/account" className="btn btn-dark" onClick={() => setOpen(false)}>
            האזור שלי
          </Link>
        ) : (
          <>
            <Link href="/login" onClick={() => setOpen(false)}>
              כניסה
            </Link>
            <Link href="/login" className="btn btn-dark" onClick={() => setOpen(false)}>
              הרשמה חינם
            </Link>
          </>
        )}
      </div>
    </header>
  );
}
