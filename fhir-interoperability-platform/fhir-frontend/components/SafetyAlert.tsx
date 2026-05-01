

export default function SafetyAlert() {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 h-full overflow-hidden">
      <div className="p-4 border-b border-zinc-100">
        <h3 className="text-sm font-bold text-[#4A5568] uppercase tracking-tight">
          Safety Alerts
        </h3>
      </div>

      {/* placeholder for future safety alert integration */}
      <div className="p-6">
        <p className="text-[13px] leading-relaxed text-zinc-500 italic">
          No clinical safety alerts or high-risk interactions have been identified 
          from the integrated data sources for this patient record.
        </p>
      </div>
    </div>
  );
}