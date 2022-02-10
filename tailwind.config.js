const colors = require('tailwindcss/colors')

module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [
    'trip_planner/templates/**/*.html',
    'trip_planner/tailwind.py',
    'assets/js/tailwind.json'
  ],
  theme: {
    extend: {
      colors: {
        teal: colors.teal,
        gray: colors.trueGray,
        indigo: colors.indigo,
        orange: colors.orange  
      },
      flex: {
        'grow': '1 0 auto',
        'grow-half-1': '1 0 50%',
        'shrink-trip-app': '0 1 26rem'
      },
      minWidth: {
        'wide': '40rem'
      },
      minHeight: {
        '60vh': '60vh'
      },
      maxHeight: {
        'body-sans-header': 'calc(100vh - 8rem)',
        'three-quarters-screen': '75vh'
      },
      gridTemplateColumns: {
        'auto-20rem': 'repeat(auto-fill, minmax(20rem, 1fr))'
      }
    },
  },
  variants: {},
  plugins: [],
}
