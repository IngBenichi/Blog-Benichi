/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./blog/templates/**/*.html",
    "./blog/**/*.py",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ff4803',
        secondary: '#FF1A03',
      }
    },
  },
  plugins: [],
};