const colors = require('tailwindcss/colors')

module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
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
      maxHeight: {
        'almost-screen': '90vh'
      },
      gridTemplateColumns: {
        'auto-20rem': 'repeat(auto-fill, minmax(20rem, 1fr))'
      }
    },
  },
  variants: {},
  plugins: [],
}
