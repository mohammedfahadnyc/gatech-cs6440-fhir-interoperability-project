"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import PatientTable from "@/components/PatientTable";

export default function MyPatientsPage() {
  const [isClinician, setIsClinician] = useState(false);
  const router = useRouter();



    useEffect(() => {
    const role = localStorage.getItem("user_role");
    
    if (!role || role.toLowerCase() !== "clinician") {
        console.log("Access denied. Role found:", role);
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
          <h1 className="text-2xl font-bold text-zinc-800">My Patients</h1>
          <p className="text-zinc-500 text-sm font-medium">Clinical Directory</p>
        </header>
        <PatientTable />
      </div>
    </main>
  );
}