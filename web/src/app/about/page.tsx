import type { Metadata } from "next";
import Link from "next/link";
import Blobs from "@/components/Blobs";
import { IconArrow } from "@/components/Icons";

export const metadata: Metadata = { title: "עליי", description: "מי עומד מאחורי Free AI ולמה הכל בחינם." };

export default function About() {
  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <Blobs preset="hero" />
      <div className="container split" style={{ position: "relative" }}>
        <div className="head" data-reveal style={{ margin: 0 }}>
          <span className="tag">עליי</span>
          <h1>היי, אני שי.</h1>
          <p>ראיתי איך קורסי AI בעברית נמכרים באלפי שקלים, ואיך בעלי עסקים, פרילנסרים וסקרנים מוותרים בגלל המחיר.</p>
          <p>אז פתחתי את Free AI: כל הידע – Claude, Lovable, סוכנים ואוטומציות – בעברית, צעד אחרי צעד, ובחינם. לתמיד.</p>
          <Link href="/courses/claude" className="btn btn-dark" style={{ alignSelf: "flex-start" }}>
            מתחילים ללמוד <IconArrow />
          </Link>
        </div>
        <div className="glass" data-reveal style={{ aspectRatio: "4/5", maxWidth: 420, width: "100%", justifySelf: "center", display: "grid", placeItems: "center", fontSize: 96, fontWeight: 900, color: "var(--ink-3)" }}>
          ש
        </div>
      </div>
    </section>
  );
}
