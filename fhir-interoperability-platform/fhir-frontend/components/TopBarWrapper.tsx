"use client";

import { usePathname } from "next/navigation";
import TopBar from "./TopBar";

export default function TopBarWrapper() {
  const pathname = usePathname();
  const isLoginPage = pathname === "/login";

  if (isLoginPage) return null;
  return <TopBar />;
}