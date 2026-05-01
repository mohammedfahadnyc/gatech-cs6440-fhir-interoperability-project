"use client"; 

import { useEffect, useState } from "react";
import { fhirService } from "../services/fhirService";
import QuickProfile from "../components/QuickProfile";
import MedicationProfile from "../components/MedicationProfile";
import HbA1cTable from "../components/HbA1cTable";
import SafetyAlert from "../components/SafetyAlert";
import AuthorizeButton from "@/components/AuthorizeButton";

export default function Home() {
  const [role, setRole] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const patient_id = localStorage.getItem("patient_id");

  useEffect(() => {
    const savedRole = localStorage.getItem("user_role") || "Clinician";
    setRole(savedRole);

    const handleLoadTest = async (e: any) => {
      setLoading(true);
      try {
        const patientId = e.detail.id; // temporarily loading patient =1 
        const clinicalData = await fhirService.getFullDashboardData(patientId);
        setData(clinicalData);
      } catch (err) {
        console.error("Failed to load test data", err);
      } finally {
        setLoading(false);
      }
    };

    window.addEventListener("load-test-patient", handleLoadTest);
    return () => window.removeEventListener("load-test-patient", handleLoadTest);
  }, []);

  // loading state
  if (loading) {
    return <div className="p-10 text-zinc-500 font-medium">Fetching clinical data for Patient 1...</div>;
  }

  // clinical data view
  if (data) {
    return (
      <main className="p-10 w-full animate-in fade-in duration-500">
        <div className="max-w-7xl mx-auto flex flex-col gap-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
            <QuickProfile patient={data.patient} />
            <MedicationProfile medications={data.medications} source={data.patient.source}/>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
            <HbA1cTable data={data.hba1cTrend} />
            <SafetyAlert />
          </div>
        </div>
      </main>
    );
  }

  // default dashboard view
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <h1 className="text-[40px] font-bold text-[#2D3748] capitalize mb-2">
        {role} Dashboard
      </h1>
    </div>
  );
}
import Image from "next/image";