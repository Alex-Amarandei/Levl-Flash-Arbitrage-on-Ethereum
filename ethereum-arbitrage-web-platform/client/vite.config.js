import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
    server: {
        proxy: {
            "/server": {
                target: "http://localhost:5000",
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path.replace(/^\/server/, ""),
            },
        },
    },
    plugins: [react()],
});