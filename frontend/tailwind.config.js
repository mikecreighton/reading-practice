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

            "button-option-hover": colors.white,
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
              primary: colors.purple["950"],
              secondary: "#87CEEB",
              accent: "#FF69B4",
              background: colors.pink["200"],
              text: colors.indigo["950"],

              "bottom-bar": colors.pink["100"],
              story: colors.pink["200"],
              "story-illustration-border": colors.pink["300"],

              chip: colors.pink["300"],
              "chip-text": colors.indigo["950"],

              "button-primary": colors.purple["950"],
              "button-primary-text": colors.pink["50"],
              "button-primary-border": colors.purple["950"],
              "button-primary-hover": colors.purple["900"],

              "button-secondary": colors.pink["200"],
              "button-secondary-text": colors.indigo["950"],
              "button-secondary-border": colors.pink["200"],

              "button-secondary-hover": colors.pink["300"],
              "button-secondary-hover-text": colors.indigo["950"],
              "button-secondary-hover-border": colors.pink["300"],

              "button-option": colors.pink["100"],
              "button-option-text": colors.indigo["950"],
              "button-option-border": colors.pink["100"],

              "button-option-hover": colors.pink["50"],
              "button-option-hover-text": colors.indigo["950"],
              "button-option-hover-border": colors.pink["300"],

              "button-option-selected": colors.pink["50"],
              "button-option-selected-text": colors.indigo["950"],
              "button-option-selected-border": colors.pink["400"],

              "input-border": colors.pink["100"],
              "input-background": colors.pink["100"],
              "input-border-focus": colors.pink["400"],
              "input-background-focus": colors.pink["50"],
              "input-text": colors.indigo["950"],
              "input-placeholder": colors.pink["300"],
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
              "story-illustration-border": "#28661E",

              chip: "#9BD49E",
              "chip-text": "#041604",

              "button-primary": "#FFD700",
              "button-primary-text": "#0A1F0A",
              "button-primary-border": "#FFD700",
              "button-primary-hover": "#FFE34D",

              "button-secondary": "#4CAF50",
              "button-secondary-text": "#041604",
              "button-secondary-border": "#4CAF50",

              "button-secondary-hover": "#47A44B",
              "button-secondary-hover-text": "#0A1F0A",
              "button-secondary-hover-border": "#47A44B",

              "button-option": "#4CAF50",
              "button-option-text": "#041604",
              "button-option-border": "#4CAF50",

              "button-option-hover": colors.pink["50"],
              "button-option-hover-text": colors.indigo["950"],
              "button-option-hover-border": colors.pink["300"],

              "button-option-selected": "#9BD49E",
              "button-option-selected-text": "#041604",
              "button-option-selected-border": "#429946",

              "input-border": "#2E7D32",
              "input-background": "#4CAF50",
              "input-border-focus": "#ADDBAF",
              "input-background-focus": "#9BD49E",
              "input-text": "#041604",
              "input-placeholder": "#28661E",
            },
          },
        },
      ],
    }),
  ],
}
