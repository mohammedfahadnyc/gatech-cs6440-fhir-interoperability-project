"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();



  const menuItems = [
    { label: "Dashboard", path: "/" },
    { label: "My Patients", path: "/patients" }, 
    { label: "Appointment", path: "/appointments" },
    { label: "Calendar", path: "/calendar" },
    { label: "Messages", path: "/messages", badge: 1 },
    { label: "Settings", path: "/settings" },
  ];

  return (
    <aside className="w-60 bg-[#F8F9FB] border-r border-zinc-200 h-full py-8 flex flex-col">
      <nav className="flex flex-col gap-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.path;

          return (
            <Link
              href={item.path}
              key={item.label}
              className={`px-8 py-3 flex items-center justify-between cursor-pointer text-sm font-medium transition-colors ${
                isActive 
                  ? "text-blue-600 border-r-2 border-blue-600 bg-white" 
                  : "text-zinc-500 hover:bg-zinc-100"
              }`}
            >
              <span>{item.label}</span>
              {item.badge && (
                <span className="bg-rose-500 text-white text-[10px] w-5 h-5 flex items-center justify-center rounded-full">
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}


      </nav>
      
      <div className="mt-auto px-8">
        <button 
          onClick={() => {
            localStorage.clear();
            window.location.href = "/login";
          }}
          className="text-zinc-400 text-xs hover:text-rose-500 transition-colors"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}