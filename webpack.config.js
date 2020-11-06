const path = require('path');

module.exports = {
    entry: {
        map: './assets/js/map.js',
        point_form: './assets/js/point_form.js'
    },
    output: {
        path: path.resolve(__dirname, 'trip_planner/static/js'),
        filename: '[name].js',
        publicPath: '/static/js/'
    },
    devtool: 'cheap-module-source-map',
    optimization: {
        usedExports: true,
        splitChunks: {
            chunks: 'all',
            name: 'vendor',
            cacheGroups: {
                bsb: {
                    test: /\/node_modules\/bs-platform\//,
                    name: 'vendor-bsb'
                }
            }
        }
    }
}
