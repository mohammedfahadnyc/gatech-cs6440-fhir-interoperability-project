"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Image from "next/image";

interface LoginResponse {
  token: string;
  user: {
    id: number;
    email: string;
    role: string;
    patient_id: number | null;
    created_at: string;
  };
}

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
        const response = await axios.post<LoginResponse>(
          `/api/fhir/auth/login`,
          { email, password }
        );


        if (response.data.token) {
        localStorage.setItem("fhir_token", response.data.token);

        localStorage.setItem("patient_id", response.data.user.patient_id)

        const userRole = response.data.user.role;
        localStorage.setItem("user_role", userRole);

        router.push("/");
        }
    } catch (err: any) {
      setError("Invalid email or password. Please try again.");
      console.error("Login Error:", err.response?.data || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white px-6">
      {/* logo */}
      <div className="mb-8">
        <div className="w-32 h-32 rounded-full border-4 border-[#8EB3E2] flex items-center justify-center relative overflow-hidden bg-white shadow-sm">
          <Image
            src="/logo.jpg"
            alt="Clinic Logo"
            fill
            className="object-contain p-2"
            priority
          />
        </div>
      </div>

      <div className="w-full max-w-[360px]">
        <h1 className="text-[32px] font-bold text-[#2D3748] leading-tight">Login</h1>
        <p className="text-[20px] text-[#4A5568] mb-10">to get started</p>

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-4">
            <input
              type="email"
              placeholder="email address"
              className="w-full p-4 border border-zinc-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-zinc-600 placeholder-zinc-300"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="password"
              className="w-full p-4 border border-zinc-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-zinc-600 placeholder-zinc-300"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="text-left py-2">
            <button type="button" className="text-zinc-400 text-sm hover:text-zinc-600 transition-colors">
              Forgot Password?
            </button>
          </div>

          {error && <p className="text-red-500 text-xs italic text-center">{error}</p>}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-[#3D4FE0] text-white font-bold py-4 rounded-xl hover:bg-blue-700 transition-colors mt-2 disabled:bg-zinc-300"
          >
            {isLoading ? "Signing in..." : "Continue"}
          </button>
        </form>

        <p className="mt-10 text-center text-zinc-400 text-sm">
          New User? <button className="font-bold text-zinc-700 hover:underline">Register</button>
        </p>
      </div>
    </div>
  );
}