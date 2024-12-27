/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      screens: {
        sm: '614px',
        md: '1214px',
        lg: '1514px',
      },
    },
  },
  plugins: [],
};
