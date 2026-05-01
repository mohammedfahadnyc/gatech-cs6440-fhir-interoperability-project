"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fhirService } from "../services/fhirService"; 

export default function PatientTable() {
    const [patients, setPatients] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const loadList = async () => {
        try {
        const data = await fhirService.getPatients();
        setPatients(data);
        } catch (err) {
        console.error("Failed to fetch patient list:", err);
        } finally {
        setLoading(false);
        }
    };


    useEffect(() => { loadList(); }, []);

    const handleImport = async (id: string) => {
        await fhirService.importPatient(id);
        loadList(); 
    };

    if (loading) return <div className="p-10 text-zinc-400 animate-pulse font-medium">Loading Patient Directory...</div>;

    return (
        <div className="bg-white rounded-xl shadow-sm border border-zinc-200 overflow-hidden">
        <table className="w-full text-left">
            <thead className="bg-[#F8F9FB] border-b border-zinc-200">
            <tr>
                <th className="px-6 py-4 text-[10px] font-bold text-zinc-400 uppercase">Patient Name</th>
                
                <th className="px-6 py-4 text-[10px] font-bold text-zinc-400 uppercase">Origin</th>
                <th className="px-6 py-4 text-[10px] font-bold text-zinc-400 uppercase text-right">Action</th>
            </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
            {patients.map((p) => {
                const isInternal = p.data_origin === "internal";
                const isImported = p.imported === true;
                const isAuthorized = p.authorized === true;

                return (
                <tr key={p.id} className="hover:bg-blue-50/40 transition-colors">
                    <td className="px-6 py-4">
                    <div className="flex flex-col">
                        <span className="text-sm font-bold text-zinc-800">{p.name}</span>
                        <span className="text-[10px] text-zinc-400 font-mono">#{p.id}</span>
                    </div>
                    </td>
                    <td className="px-6 py-4">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isInternal ? "bg-blue-50 text-blue-600" : "bg-purple-50 text-purple-600"
                    }`}>
                        {p.data_origin.toUpperCase()}
                    </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                    {/* decision logic starts here */}
                    {isInternal || isImported ? (
                        <Link href={`/patients/${p.id}`} className="text-xs font-bold text-blue-600 underline uppercase">
                        View Chart →
                        </Link>
                    ) : !isAuthorized ? (
                        <span className="text-[10px] text-zinc-400 italic">Awaiting Authorization</span>
                    ) : (
                        <button 
                        onClick={() => handleImport(p.id.toString())}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-[10px] font-bold hover:bg-blue-700 transition-colors"
                        >
                        IMPORT FROM {p.source?.toUpperCase() || "EXTERNAL"}
                        </button>
                    )}
                    </td>
                </tr>
                );
            })}
            </tbody>
        </table>
    </div>
  );
}