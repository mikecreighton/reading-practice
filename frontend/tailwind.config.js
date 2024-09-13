/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors")

export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [
    require("tailwindcss-themer")({
      defaultTheme: {
        extend: {
          dropShadow: {
            bar: "0 -2px 10px rgba(0, 0, 0, 0.1)",
          },
          colors: {
            transparent: "transparent",
            current: "currentColor",
            black: colors.black,
            white: colors.white,
            gray: colors.gray,

            primary: colors.gray["800"],
            secondary: colors.gray["400"],
            background: colors.white,
            text: colors.gray["800"],

            "button-primary": colors.gray["800"],
            "button-primary-text": colors.white,
            "button-primary-border": colors.gray["800"],
            "button-primary-hover": colors.gray["700"],

            "button-secondary": colors.gray["300"],
            "button-secondary-hover": colors.gray["200"],
            "button-secondary-text": colors.gray["800"],
            "button-secondary-border": colors.gray["400"],

            "input-border": colors.gray["300"],
            "input-background": colors.gray["100"],
            "input-border-focus": colors.gray["600"],
            "input-text": colors.gray["800"],
            "input-placeholder": colors.gray["400"],
          },
        },
      },
      themes: [
        {
          name: "bubblegum",
          selectors: [".bubblegum", ".theme-bubblegum"],
          extend: {
            colors: {
              primary: "#FF69B4", // Bubblegum pink
              secondary: "#87CEEB", // Sky blue
              accent: "#98FB98", // Pale green
              background: "#FFF0F5", // Lavender blush
              text: "#4B0082", // Indigo

              "button-primary": "#FF69B4",
              "button-primary-text": "#FFF0F5",
              "button-primary-border": "#FF69B4",
              "button-primary-hover": "#FFB6C1",

              "button-secondary": "#87CEEB",
              "button-secondary-hover": "#66B2FF",
              "button-secondary-text": "#4B0082",
              "button-secondary-border": "#4B0082",

              "input-border": "#87CEEB",
              "input-background": "#FFFFFF",
              "input-border-focus": "#4B0082",
              "input-text": "#4B0082",
              "input-placeholder": "#87CEEB",
            },
          },
        },
        {
          name: "adventure",
          selectors: [".adventure", ".theme-adventure"],
          extend: {
            colors: {
              primary: "#FF69B4", // Bubblegum pink
              secondary: "#87CEEB", // Sky blue
              accent: "#98FB98", // Pale green
              background: "#FFF0F5", // Lavender blush
              text: "#4B0082", // Indigo
            },
          },
        },
      ],
    }),
  ],
}
