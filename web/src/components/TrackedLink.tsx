"use client";

import { usePathname, useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { trackEvent } from "@/lib/track";
import { loginHref, useUser } from "@/lib/useUser";

/** קישור יוצא שנספר. kind=download דורש משתמש מחובר */
export default function TrackedLink({ href, kind = "click", className, children, sponsored }: { href: string; kind?: "click" | "download"; className?: string; children: ReactNode; sponsored?: boolean }) {
  const user = useUser();
  const path = usePathname();
  const router = useRouter();
  return (
    <a
      href={href}
      className={className}
      target="_blank"
      rel={sponsored ? "noopener sponsored" : "noopener"}
      onClick={(e) => {
        if (kind === "download" && !user) {
          e.preventDefault();
          router.push(loginHref(path));
          return;
        }
        trackEvent(kind, href);
      }}
    >
      {children}
    </a>
  );
}
