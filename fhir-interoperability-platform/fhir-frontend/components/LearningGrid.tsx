import { useState } from "react";
export default function LearningGrid() {
  const lessons = [
    "What is Diabetes?",
    "Type 1 & Type 2",
    "Diet and Exercise",
    "Medications to Treat Diabetes",
    "The Role of Insulin",
    "Oral Hygiene",
    "Footcare",
    "Complications",
  ];
  const [checked, setChecked] = useState<boolean[]>(
    new Array(lessons.length).fill(false)
  );

  const toggle = (index: number) => {
    const updated = [...checked];
    updated[index] = !updated[index];
    setChecked(updated);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6 text-left text-gray-600">
        Learning Portal
      </h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {lessons.map((lesson, index) => (
          <div key={index} className="relative bg-white rounded-2xl shadow-md p-6 cursor-pointer transition hover:shadow-xl hover:-translate-y-1">
            <div
              onClick={(e) => {
                e.stopPropagation();
                toggle(index);
              }}
              className={`absolute top-4 right-4 w-6 h-6 flex items-center justify-center rounded-full border-2 cursor-pointer transition
                ${
                  checked[index]
                    ? "border-green-500 bg-green-500"
                    : "border-gray-300 bg-white"
                }`}
            >
              <span
                className={`text-sm font-bold ${
                  checked[index] ? "text-white" : "text-gray-400"
                }`}
              >
                
              </span>
            </div>
            <h2 className="text-lg font-medium">{lesson}</h2>
            <div className="w-full h-px bg-gray-200 my-3" />
            <p className="text-sm text-gray-500">
              Click to start this lesson
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}