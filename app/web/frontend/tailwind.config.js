/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#a13b3e',
          DEFAULT: '#701516',
          dark: '#5c0f10',
          hover: '#8e2b28'
        }
      }
    },
  },
  plugins: [],
}
