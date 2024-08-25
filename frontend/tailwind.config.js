/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('tailwindcss-themer')({
      defaultTheme: {
        extend: {
          colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: colors.black,
            white: colors.white,
            gray: colors.gray,
            primary: colors.gray["800"],
            secondary: colors.gray["400"],
            'input-border': colors.gray["300"],
            'input-background': colors.gray["100"],
            'input-border-focus': colors.gray["600"],
          },
        },
      },
      themes: [
        {
          name: 'bubblegum',
          extend: {
            colors: {
              primary: '#FF69B4',    // Bubblegum pink
              secondary: '#87CEEB',  // Sky blue
              accent: '#98FB98',     // Pale green
              background: '#FFF0F5', // Lavender blush
              text: '#4B0082',       // Indigo
            }
          }
        }
      ]
    }),
  ],
}

