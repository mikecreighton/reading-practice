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
            background: colors.gray["200"],
            text: colors.gray["800"],

            "bottom-bar": colors.gray["100"],
            story: colors.gray["200"],
            "story-illustration-border": colors.gray["300"],

            chip: colors.gray["300"],
            "chip-text": colors.gray["800"],

            "button-primary": colors.gray["800"],
            "button-primary-text": colors.white,
            "button-primary-border": colors.gray["800"],
            "button-primary-hover": colors.gray["700"],

            "button-secondary": colors.gray["300"],
            "button-secondary-text": colors.gray["800"],
            "button-secondary-border": colors.gray["300"],

            "button-secondary-hover": colors.gray["200"],
            "button-secondary-hover-text": colors.gray["800"],
            "button-secondary-hover-border": colors.gray["400"],

            "button-option": colors.gray["50"],
            "button-option-text": colors.gray["800"],
            "button-option-border": colors.gray["50"],

            "button-option-hover": colors.gray["50"],
            "button-option-hover-text": colors.gray["800"],
            "button-option-hover-border": colors.gray["300"],

            "button-option-selected": colors.white,
            "button-option-selected-text": colors.gray["600"],
            "button-option-selected-border": colors.gray["500"], // This is for form element buttons

            "input-border": colors.gray["50"],
            "input-background": colors.gray["50"],
            "input-border-focus": colors.gray["500"],
            "input-background-focus": colors.white,
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
              primary: "#98FB98",
              secondary: "#87CEEB",
              accent: "#FF69B4",
              background: "#FFB6DA",
              text: "#4B0082",
              "bottom-bar": "#FF80BF",

              story: "#FFB6DA",

              "button-primary": "#98FB98",
              "button-primary-text": "#215921",
              "button-primary-border": "#8CF88C",
              "button-primary-hover": "#ACFCAC",

              "button-secondary": "#FFD6EA",
              "button-secondary-text": "#971958",
              "button-secondary-border": "#E285B4",

              "button-secondary-hover": "#B5E1F3",
              "button-secondary-hover-text": "#0E6386",
              "button-secondary-hover-border": "#3AA4CF",

              "button-secondary-selected": "#B5E1F3", // This is for form element buttons
              "button-secondary-selected-text": "#0E6386",
              "button-secondary-selected-border": "#3AA4CF", // This is for form element buttons

              "input-border": "#E285B4",
              "input-background": "#FFD6EA",
              "input-border-focus": "#D33484",
              "input-text": "#4B0082",
              "input-placeholder": "#D275C6",

              chip: "#B5E1F3",
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
              background: "#0F2E0F", // Very dark green
              text: "#E0F2E0", // Light mint green
              "bottom-bar": "#78C47B",

              story: "#429946",

              "button-primary": "#FFD700",
              "button-primary-text": "#0A1F0A",
              "button-primary-border": "#EBC80A",
              "button-primary-hover": "#FFE34D",

              "button-secondary": "#4CAF50",
              "button-secondary-text": "#041604",
              "button-secondary-border": "#429946",

              "button-secondary-hover": "#47A44B",
              "button-secondary-hover-text": "#0A1F0A",
              "button-secondary-hover-border": "#22561A",

              "button-secondary-selected": "#9BD49E", // This is for form element buttons
              "button-secondary-selected-text": "#041604",
              "button-secondary-selected-border": "#4CAF50", // This is for form element buttons

              "input-border": "#2E7D32",
              "input-background": "#4CAF50",
              "input-border-focus": "#4CAF50",
              "input-text": "#041604",
              "input-placeholder": "#28661E",

              chip: "#9BD49E",
              "chip-text": "#041604",
            },
          },
        },
      ],
    }),
  ],
}
