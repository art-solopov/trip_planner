module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
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
      }
    },
  },
  variants: {},
  plugins: [],
}
