import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "hsl(270, 80%, 55%)",
        "primary-light": "hsl(270, 80%, 65%)",
        accent: "hsl(330, 80%, 55%)",
        "accent-light": "hsl(330, 80%, 65%)",
        surface: "hsl(240, 10%, 10%)",
        "surface-light": "hsl(240, 8%, 14%)",
        background: "hsl(240, 12%, 6%)",
        muted: "hsl(240, 5%, 65%)",
      },
      fontFamily: {
        sans: ["'Outfit'", "Inter", "system-ui", "sans-serif"],
        display: ["'Outfit'", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 20px rgba(139, 92, 246, 0.15)",
        "glow-lg": "0 0 40px rgba(139, 92, 246, 0.25)",
        "glow-accent": "0 0 20px rgba(236, 72, 153, 0.15)",
      },
      animation: {
        "fade-in-up": "fadeInUp 0.6s ease-out forwards",
        "fade-in": "fadeIn 0.5s ease-out forwards",
        "pulse-glow": "pulseGlow 3s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
export default config;
