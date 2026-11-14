import type { Metadata, Viewport } from "next";
import { Heebo } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Reveal from "@/components/Reveal";
import WhatsApp from "@/components/WhatsApp";
import { site } from "@/content/site";

const heebo = Heebo({ variable: "--font-heebo", subsets: ["hebrew", "latin"] });

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: { default: `${site.name} – ${site.tagline}`, template: `%s | ${site.name}` },
  description: site.description,
  openGraph: { siteName: site.name, locale: "he_IL", type: "website" },
};

export const viewport: Viewport = { themeColor: "#ffffff" };

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="he" dir="rtl" className={heebo.variable}>
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
        <WhatsApp />
        <Reveal />
      </body>
    </html>
  );
}
