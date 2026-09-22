import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// During local `npm run dev`, proxy /api to the backend container/host.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
