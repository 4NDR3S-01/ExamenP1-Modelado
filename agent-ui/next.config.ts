import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  devIndicators: false,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:7777/api/:path*', // Proxy a FastAPI
      },
    ]
  },
}

export default nextConfig
