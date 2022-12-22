/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.jinja2", "./src/**/*.json"],
  theme: {
    fontFamily: {
      playfair: ["Playfair Display", "serif"],
      poppins: ["Poppins", "sans-serif"],
    },
    extend: {
      colors: {
        primary: "#cc0000",
        secondary: "#fed7d7",
      },
      gridTemplateColumns: {
        categories: "repeat(auto-fit, minmax(320px, 1fr))",
        subcategories: "repeat(auto-fit, minmax(250px, 1fr))",
      },
    },
  },
};
