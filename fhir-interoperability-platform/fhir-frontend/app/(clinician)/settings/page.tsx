"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function PlaceholderPage() {
  const [isClinician, setIsClinician] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const role = localStorage.getItem("user_role");
    if (!role || role.toLowerCase() !== "clinician") {
      router.push("/");
    } else {
      setIsClinician(true);
    }
  }, [router]);

  if (!isClinician) return null;

  return (
    <main className="p-10 w-full animate-in fade-in duration-500">
      <div className="max-w-7xl mx-auto flex flex-col gap-8">
        <header>
          <h1 className="text-2xl font-bold text-zinc-800">Settings</h1>
          <p className="text-zinc-500 text-sm font-medium"></p>
        </header>
        
        <div className="bg-white rounded-xl shadow-sm border border-zinc-200 p-20 flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 bg-zinc-50 rounded-full flex items-center justify-center mb-4">
                <span className="text-2xl">🛠️</span>
            </div>
            <h2 className="text-lg font-bold text-zinc-800">Coming Soon</h2>
        </div>
      </div>
    </main>
  );
}