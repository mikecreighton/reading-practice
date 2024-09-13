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
            "bottom-bar": colors.white,

            "button-primary": colors.gray["800"],
            "button-primary-text": colors.white,
            "button-primary-border": colors.gray["800"],
            "button-primary-hover": colors.gray["700"],

            "button-secondary": colors.white,
            "button-secondary-hover": colors.gray["200"],
            "button-secondary-hover-text": colors.gray["800"],
            "button-secondary-border": colors.gray["400"], // This is for form element buttons
            "button-secondary-selected": colors.gray["200"], // This is for form element buttons
            "button-secondary-selected-border": colors.gray["400"], // This is for form element buttons
            "button-secondary-selected-text": colors.gray["600"],
            "button-secondary-text": colors.gray["800"],
            "button-secondary-border": colors.gray["400"],

            "input-border": colors.gray["400"],
            "input-background": colors.gray["100"],
            "input-border-focus": colors.gray["600"],
            "input-text": colors.gray["800"],
            "input-placeholder": colors.gray["400"],

            "chip": colors.gray["200"],
            "chip-text": colors.gray["800"],
          },
        },
      },
      themes: [
        {
          name: "bubblegum",
          selectors: [".bubblegum", ".theme-bubblegum"],
          extend: {
            colors: {
              primary: "#98FB98",
              secondary: "#87CEEB",
              accent: "#FF69B4",
              background: "#FFB6DA",
              text: "#4B0082",
              "bottom-bar": "#FF80BF",

              "button-primary": "#98FB98",
              "button-primary-text": "#215921",
              "button-primary-border": "#8CF88C",
              "button-primary-hover": "#ACFCAC",

              "button-secondary": "#FFD6EA",
              "button-secondary-hover": "#B5E1F3",
              "button-secondary-hover-text": "#0E6386",
              "button-secondary-hover-border": "#3AA4CF",
              "button-secondary-selected": "#B5E1F3", // This is for form element buttons
              "button-secondary-selected-border": "#3AA4CF", // This is for form element buttons
              "button-secondary-selected-text": "#0E6386",
              "button-secondary-text": "#971958",
              "button-secondary-border": "#E285B4",

              "input-border": "#E285B4",
              "input-background": "#FFD6EA",
              "input-border-focus": "#D33484",
              "input-text": "#4B0082",
              "input-placeholder": "#87CEEB",

              "chip": '#B5E1F3',
              "chip-text": "#0E6386",
            },
          },
        },
        {
          name: "adventure",
          selectors: [".adventure", ".theme-adventure"],
          extend: {
            colors: {
              primary: "#1A4314", // Deep jungle green
              secondary: "#FFD700", // Golden yellow
              accent: "#4CAF50", // Vibrant green
              background: "#0A1F0A", // Very dark green
              text: "#E0F2E0", // Light mint green

              "button-primary": "#4CAF50",
              "button-primary-text": "#0A1F0A",
              "button-primary-border": "#4CAF50",
              "button-primary-hover": "#45A049",

              "button-secondary": "#FFD700",
              "button-secondary-hover": "#FFC107",
              "button-secondary-text": "#0A1F0A",
              "button-secondary-border": "#FFD700",

              "input-border": "#2E7D32",
              "input-background": "#1B5E20",
              "input-border-focus": "#4CAF50",
              "input-text": "#E0F2E0",
              "input-placeholder": "#81C784",
            },
          },
        },
      ],
    }),
  ],
}
