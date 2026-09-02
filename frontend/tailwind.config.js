/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#8B4513',  // Chocolate brown
        secondary: '#D2691E', // Chocolate
        accent: '#FFD700',   // Gold
      }
    },
  },
  plugins: [],
}
