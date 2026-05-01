/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/fhir/:path*',
        destination: 'https://fhir-backend-qrq8.onrender.com/:path*',
      },
    ]
  },
}

export default nextConfig