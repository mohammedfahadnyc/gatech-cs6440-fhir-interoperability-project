export default function ConditionsList({ conditions }: { conditions: any[] }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 overflow-hidden h-full">
      <div className="p-4 border-b border-zinc-100">
        <h3 className="text-sm font-bold text-[#4A5568] uppercase tracking-tight">Active Diagnoses</h3>
      </div>
      <div className="p-0">
        {conditions?.map((cond) => (
          <div key={cond.id} className="px-6 py-4 flex items-center justify-between border-b last:border-0 border-zinc-50">
            <div>
              <p className="text-sm font-bold text-zinc-800">{cond.code.text}</p>
              <p className="text-[10px] text-zinc-400 italic">Recorded: {cond.recordedDate}</p>
            </div>
            <span className="bg-emerald-50 text-emerald-600 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">
              {cond.clinicalStatus.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}