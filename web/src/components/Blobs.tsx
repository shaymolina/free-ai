type Blob = { c: "b" | "p" | "k"; x: string; y: string; s: number };

const presets: Record<string, Blob[]> = {
  hero: [
    { c: "b", x: "-6%", y: "10%", s: 460 },
    { c: "p", x: "18%", y: "45%", s: 420 },
    { c: "k", x: "2%", y: "70%", s: 360 },
  ],
  a: [
    { c: "b", x: "70%", y: "-10%", s: 420 },
    { c: "p", x: "-5%", y: "50%", s: 380 },
  ],
  b: [
    { c: "k", x: "40%", y: "0%", s: 380 },
    { c: "p", x: "75%", y: "55%", s: 340 },
  ],
  c: [
    { c: "b", x: "10%", y: "20%", s: 360 },
    { c: "k", x: "65%", y: "40%", s: 380 },
  ],
};

export default function Blobs({ preset = "a" }: { preset?: keyof typeof presets }) {
  return (
    <div className="blobs" aria-hidden>
      {presets[preset].map((b, i) => (
        <span
          key={i}
          className={`blob ${b.c}`}
          style={{ left: b.x, top: b.y, width: b.s, height: b.s, animationDelay: `${-i * 5}s` }}
        />
      ))}
    </div>
  );
}
