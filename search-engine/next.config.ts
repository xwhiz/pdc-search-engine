import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: ["local-origin.dev", "*.local-origin.dev"],
  async rewrites() {
    return [
      {
        source: "/solr/:path*",
        destination: "http://10.7.92.170:8983/solr/:path*",
      },
    ];
  },
};

export default nextConfig;
