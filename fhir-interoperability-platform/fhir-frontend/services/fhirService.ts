import axios from 'axios';
import { mapPatientData, mapMedications, mapObservations } from '../utils/fhirMappers';

interface PatientChart {
  patient: any;
  medications: any[];
  observations: any[];
  conditions?: any[];
  notes?: any[];
}

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_FHIR_BASE_URL,
});


api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem("fhir_token") : null;

  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    console.warn("No token found in localStorage.");
  }

  return config;
}, (error) => {
  return Promise.reject(error);
});


export const fhirService = {
  getPatients: async (): Promise<any[]> => {
    const response = await api.get<any[]>('/patients'); 
    return response.data;
  },
  

  importPatient: async (id: string): Promise<any> => {
    const response = await api.post<any>(`/patients/${id}/import`);
    return response.data;
  },

  
  resetPatientData: async (id: string) => {
    await api.delete(`/patients/${id}/data`);
  },

  getFullDashboardData: async (patientId: string) => {
    try {
      
      const [chartRes, summaryRes] = await Promise.all([
        api.get<PatientChart>(`/patients/${patientId}/chart`),
        api.get<any>(`/patients/${patientId}/summary`)
      ]);

      const chart = chartRes.data;
      const summary = summaryRes.data;

      return {
        patient: {
          ...chart.patient,
          age: 2026 - new Date(chart.patient.dob).getFullYear(),
          lastA1c: summary.latest_a1c,
          data_origin: chart.patient.data_origin,
          imported: chart.patient.imported,
          source: chart.patient.source
        },
        medications: mapMedications(chart.medications),
        hba1cTrend: mapObservations(chart.observations),
      };
    } catch (error) {
      console.error("Error fetching patient data:", error);
      return null;
    }
  }
};