import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
	plugins: [react()],
	resolve: {
		alias: [
			{ find: /^react-dom$/, replacement: "react-dom/profiling" },
			{ find: "scheduler/tracing", replacement: "scheduler/tracing-profiling" },
		],
	},
	build: {
		sourcemap: true,
	},
	define: {
		"process.env.NODE_ENV": JSON.stringify("development"),
	},
});
