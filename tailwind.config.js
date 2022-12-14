/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.jinja2"],
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
        categories: "repeat(auto-fit, minmax(350px, 1fr))",
      },
    },
  },
  plugins: [require("tailwindcss-scoped-groups")],
};
