"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { fhirService } from "@/services/fhirService";
import QuickProfile from "@/components/QuickProfile";
import MedicationProfile from "@/components/MedicationProfile";
import HbA1cTable from "@/components/HbA1cTable";
import SafetyAlert from "@/components/SafetyAlert";
import ConditionsList from "@/components/ConditionsList";
import ClinicalNotes from "@/components/ClinicalNotes";
import DataManagement from "@/components/DataManagement"; 

export default function PatientDashboardPage() {
  const { id } = useParams(); 
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const clinicalData = await fhirService.getFullDashboardData(id as string);
      setData(clinicalData);
      setLoading(false);
    }
    load();
  }, [id]);
    
  if (loading) return <div className="p-10 text-zinc-500 font-medium animate-pulse">Loading Patient #{id}...</div>;
  if (!data) return <div className="p-10 text-rose-500">Error: Could not find record for Patient #{id}</div>;

  return (
    <main className="p-10 w-full animate-in fade-in duration-500">
      <div className="max-w-7xl mx-auto flex flex-col gap-8">
        
        <div className="mb-2">
          <a href="/patients" className="text-[10px] font-bold text-zinc-400 hover:text-zinc-800 uppercase tracking-widest transition-colors">
            ← Back to Directory
          </a>
        </div>


        {data.patient.imported && (
          <div className="bg-blue-50 border border-blue-100 p-3 rounded-lg text-blue-700 text-xs font-bold">
            Data Source: {data.patient.source?.toUpperCase()}
          </div>
        )}


        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          <QuickProfile patient={data.patient} />
          <MedicationProfile medications={data.medications} />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          <HbA1cTable data={data.hba1cTrend} />
          <ConditionsList conditions={data.conditions} /> 
        </div>

        <ClinicalNotes notes={data.notes} />
        <SafetyAlert />

        {data.patient.data_origin === "external" && data.patient.imported && (
          <DataManagement patientId={id as string} />
        )}      

      </div>
    </main>
  );
}