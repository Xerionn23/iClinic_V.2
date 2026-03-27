/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './**/*.js',
    './**/*.jinja',
    './**/*.jinja2',
    './**/*.twig',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0056b3',
        secondary: '#4A90E2',
        accent: '#10B981',
        'accent-light': '#34D399',
      },
    },
  },
  plugins: [],
};
