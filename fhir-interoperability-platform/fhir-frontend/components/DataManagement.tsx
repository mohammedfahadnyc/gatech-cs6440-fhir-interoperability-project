"use client";

import { useRouter } from "next/navigation";
import { fhirService } from "../services/fhirService";

interface DataManagementProps {
  patientId: string;
}
export default function DataManagement({ patientId }: DataManagementProps) {
  const router = useRouter();

  const handleReset = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to remove all imported data? This will reset the patient to an unauthorized state for demo purposes."
    );

    if (confirmed) {
      try {
        await fhirService.resetPatientData(patientId);
        router.push("/patients"); 
      } catch (error) {
        console.error("Failed to reset data:", error);
        alert("Error resetting data. Check server logs.");
      }
    }
  };

  return (
    <div className="mt-12 pt-8 border-t border-zinc-100">
      <div className="bg-rose-50/30 border border-rose-100 rounded-xl p-6 flex items-center justify-between">
        <div>
          <h4 className="text-sm font-bold text-rose-800 uppercase tracking-tight">
            Data Management (Demo Tools)

          </h4>
          <p className="text-xs text-rose-600 mt-1">

            This action will wipe all imported FHIR resources and reset the authorization status.
          </p>
        </div>
        
        <button 
          onClick={handleReset}
          className="bg-white text-rose-600 border border-rose-200 px-4 py-2 rounded-lg text-xs font-bold hover:bg-rose-600 hover:text-white transition-all shadow-sm"
        >
          Remove Imported Data
        </button>
      </div>
    </div>
  );
}