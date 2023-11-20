/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'clients/templates/**/*.html',
    'settingsapp/templates/**/*.html', // Adjust this path to match your project structure
    'home/templates/**/*.html',
    'jobs/templates/**/*.html',
    'static/preline/dist/*.js',
    "static/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },

  plugins: [
    require('preline/plugin'),
    require('flowbite/plugin')
]

};
