"use client";

import { useState, useEffect } from "react";
import axios from "axios";

type Props = {
  patientId: number;
};

export default function AuthorizeButton({ patientId }: Props) {
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState<string | null>(null);
  const storedRole = localStorage.getItem("user_role");
  // Get user role from localStorage (runs only in browser)
  useEffect(() => {
    const storedRole = localStorage.getItem("user_role");
    setRole(storedRole);
  }, []);

  const handleAuthorize = async () => {
    setLoading(true);

    try {
      const token = localStorage.getItem("fhir_token");

      const response = await axios.post(
        `/api/fhir/patients/${patientId}/authorize`,
        {
        source: "Athena"
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Authorized:", response.data);
      alert("Patient authorized successfully!");
    } catch (error: any) {
      console.error("Authorization failed:", error.response?.data || error.message);
      alert("Authorization failed");
    } finally {
      setLoading(false);
    }
  };

  if (storedRole != "patient") {
    return null;
  }

  return (
    <button
      onClick={handleAuthorize}
      disabled={loading}
      className="bg-green-600 text-white px-4 py-2 rounded-lg disabled:bg-gray-400"
    >
      {loading ? "Authorizing..." : "Authorize Medical History"}
    </button>
  );
}