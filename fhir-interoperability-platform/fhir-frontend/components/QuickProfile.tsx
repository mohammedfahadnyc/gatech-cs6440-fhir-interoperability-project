import Image from "next/image";
import AuthorizeButton from "@/components/AuthorizeButton";

interface QuickProfileProps {
  patient: {
    name: string;
    dob: string;
    gender: string;
    age: number;
    lastA1c: string | number;
  };
}


export default function QuickProfile({ patient }: QuickProfileProps) {

  const stats = [
    { label: "Last HbA1c:", value: `${patient.lastA1c}%` },
    { label: "Fasting Glucose:", value: "Pending Lab" }, //no endpoint for now. add later 
    { label: "Average Glucose (30d):", value: "Pending Lab" }, //no endpoint for now. add later 
  ];

  const patient_id = localStorage.getItem("patient_id");

  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 flex flex-col h-full">
      <div className="px-6 py-4 border-b border-dashed border-zinc-200">
        <h3 className="text-sm font-bold text-[#4A5568]">Patient's Quick Profile (Consolidated)</h3>
      </div>

      <div className="p-6 flex flex-col flex-1">
        <div className="flex gap-8 items-start mb-6">
          <div className="w-28 h-28 border border-zinc-200 rounded-sm overflow-hidden shadow-sm flex-shrink-0 relative">
            <Image
              src="/avatar.jpg" 
              alt="Patient Avatar"
              fill
              className="object-cover"
              priority 
            />
          </div>
          
          <div className="space-y-4 pt-2">
            <div className="grid grid-cols-[100px_1fr] gap-x-4 text-sm">
              <span className="text-zinc-500">Name:</span>
              <span className="font-bold text-[#2D3748] uppercase">
                {patient.name} {/* Name  from server */}
              </span>
              
              <span className="text-zinc-500">Date of Birth:</span>
              <span className="font-bold text-[#2D3748]">
                {patient.dob} <span className="font-normal text-zinc-500">(Age: {patient.age})</span>
              </span>
              
              
              <span className="text-zinc-500">Gender:</span>
              <span className="font-bold text-[#2D3748] capitalize">
                {patient.gender} {/*  Gender from server */}
              </span>
            </div>
          </div>
        </div>

        {/*  Stats Loop from server */}
        <div className="space-y-3 mb-6">
          {stats.map((stat) => (
            <div key={stat.label} className="grid grid-cols-[180px_1fr] text-sm">
              <span className="text-zinc-500">{stat.label}</span>
              <span className="font-bold text-[#2D3748]">{stat.value}</span>
            </div>
          ))}
        </div>
        
        <div className="mt-auto flex justify-end gap-3">
          <AuthorizeButton patientId={patient_id} />
          <button className="px-5 py-2 text-sm font-semibold border border-zinc-800 rounded-lg hover:bg-zinc-50 transition-colors">
            View Full Chart
          </button>

          <button className="px-5 py-2 text-sm font-semibold bg-[#E2E2E2] text-zinc-800 border border-zinc-400 rounded-lg hover:bg-zinc-300 transition-colors">
            New Notes
          </button>
        </div>
      </div>
    </div>
  );
}