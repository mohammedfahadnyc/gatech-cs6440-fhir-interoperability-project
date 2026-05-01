export default function ClinicalNotes({ notes }: { notes: any[] }) {
  const decodeNote = (base64Str: string) => {
    try {
      return atob(base64Str); 
    } catch (e) {
      return "Error decoding note content.";
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 overflow-hidden">
      <div className="p-4 border-b border-zinc-100 bg-zinc-50/50">
        <h3 className="text-sm font-bold text-[#4A5568] uppercase tracking-tight">Clinical Documentation</h3>
      </div>
      <div className="divide-y divide-zinc-100">
        {notes?.map((note) => (
          <div key={note.id} className="p-6">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-bold text-blue-600">{note.author[0].display}</span>
              <span className="text-[10px] text-zinc-400 uppercase font-mono">{new Date(note.date).toLocaleDateString()}</span>
            </div>
            <p className="text-sm text-zinc-700 leading-relaxed">
              {decodeNote(note.content[0].attachment.data)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}