export const mapPatientData = (patient: any, summary: any) => {
  if (!patient) return null;
  return {
    name: patient.name,
    dob: patient.dob,
    gender: patient.gender,
    age: new Date().getFullYear() - new Date(patient.dob).getFullYear(),
    lastA1c: summary?.latest_a1c || "N/A",
  };
};

export const mapMedications = (meds: any[]) => {
  return (meds || []).map((m) => ({
    name: m.medicationCodeableConcept?.text || "Unknown",
    dosage: "See Chart", // The Chart data doesn't have dosage strings yet
    status: m.status,
    source: "Clinical Record",
  }));
};

export const mapObservations = (obs: any[]) => {
  return (obs || [])
    .filter((o) => o.code?.text === "HbA1c")
    .map((o) => ({
      date: new Date(o.effectiveDateTime).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric'
      }),
      value: `${o.valueQuantity?.value}${o.valueQuantity?.unit}`,
      type: "Baseline Lab",
      source: "Lab Results",
    }));
};