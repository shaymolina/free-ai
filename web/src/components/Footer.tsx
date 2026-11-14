import Link from "next/link";
import { nav, site } from "@/content/site";
import { Logo } from "./Header";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="giant" aria-hidden>
          Free AI
        </div>
        <div className="footer-row">
          <Logo />
          <nav aria-label="ניווט תחתון">
            {nav.map((n) => (
              <Link key={n.href} href={n.href}>
                {n.label}
              </Link>
            ))}
            <Link href="/privacy">פרטיות</Link>
            <Link href="/terms">תנאי שימוש</Link>
          </nav>
          <span>
            © 2026 {site.name}. הכל בחינם.
          </span>
        </div>
      </div>
    </footer>
  );
}
