import type { Metadata } from "next";
import Blobs from "@/components/Blobs";
import SkillsBrowser from "@/components/SkillsBrowser";

export const metadata: Metadata = { title: "ספריית סקילים", description: "סקילים בעברית ל-Claude – מורידים, מתקינים ומשתמשים. בחינם." };

export default function Skills() {
  return (
    <>
      <section className="page-hero">
        <Blobs preset="hero" />
        <div className="container" style={{ position: "relative" }}>
          <div className="head" data-reveal>
            <span className="tag">סקילים</span>
            <h1>משדרגים את Claude בלחיצה</h1>
            <p>ספריית סקילים בעברית שעושים עבודה אמיתית. בוחרים, מורידים, מתקינים.</p>
          </div>
        </div>
      </section>
      <section className="section" style={{ paddingTop: 20 }}>
        <div className="container">
          <SkillsBrowser />
        </div>
      </section>
    </>
  );
}
