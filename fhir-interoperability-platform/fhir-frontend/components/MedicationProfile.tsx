interface Medication {
  name: string;
  dosage: string;
  status: string;
  source: string;
}


interface MedicationProfileProps {
  medications: Medication[];
  source?: string;
}

export default function MedicationProfile({ medications, source }: MedicationProfileProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 overflow-hidden h-full">
 
      <div className="p-4 border-b border-zinc-100">
        <h3 className="text-sm font-bold text-[#4A5568] uppercase tracking-tight">
          Unified Medication Profile (Consolidated)
        </h3>
      </div>

      <div className="p-0">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-zinc-500 border-b border-zinc-100">
              <th className="px-4 py-3 font-semibold">Medication</th>
              <th className="px-4 py-3 font-semibold">Dosage</th>
              <th className="px-4 py-3 font-semibold">Status</th>
              <th className="px-4 py-3 font-semibold">Source</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {/* Medication data  from Flask backend */}
            {medications && medications.length > 0 ? (
              medications.map((med, i) => (
                <tr key={i} className="text-zinc-700 hover:bg-zinc-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-zinc-900">{med.name}</td>
                  
                  {/* This is the placeholder for Dosage data */}
                  <td className="px-4 py-3 text-zinc-400 italic">N/A</td>
                  
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${
                      med.status === 'active' 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-zinc-100 text-zinc-600'
                    }`}>
                      {med.status}
                    </span>
                  </td>



                  {/* placeholder for Source data */}
                  <td className="px-4 py-3 text-zinc-400 italic text-xs">  {med.source || source || "Internal Record"} </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-zinc-400">
                  No active medications found in patient's record.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}