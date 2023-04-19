/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{jinja2,json}"],
  theme: {
    fontFamily: {
      playfair: ["Playfair Display", "serif"],
      poppins: ["Poppins", "sans-serif"],
    },
    extend: {
      screens: {
        "hover-none": { raw: "(hover: none)" },
      },
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
  plugins: ["prettier-plugin-tailwindcss", "prettier-plugin-jinja-template"],
};
