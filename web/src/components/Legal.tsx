import Blobs from "./Blobs";

export default function Legal({ title, updated, sections }: { title: string; updated: string; sections: { h: string; p: string[] }[] }) {
  return (
    <section className="page-hero" style={{ paddingBottom: 100 }}>
      <Blobs preset="a" />
      <div className="container" style={{ position: "relative" }}>
        <div className="head">
          <h1 style={{ fontSize: "clamp(34px,5vw,56px)" }}>{title}</h1>
          <p>עודכן לאחרונה: {updated}</p>
        </div>
        <div className="prose">
          {sections.map((s) => (
            <div key={s.h} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              <h2>{s.h}</h2>
              {s.p.map((t, i) => <p key={i}>{t}</p>)}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
