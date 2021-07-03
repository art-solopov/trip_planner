const path = require('path');

const webpack = require('webpack');

module.exports = {
    entry: {
        map: './assets/js/map.js',
        point_form: './assets/js/point_form.js',
        shared_app: './assets/js/shared_app.js'
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
            cacheGroups: {
                commons: {
                    name: 'commons',
                    chunks: 'initial',
                    minChunks: 2
                },
                vendor: {
                    name: 'vendor',
                    test: new RegExp('/node_modules/'),
                    chunks: 'all'
                }
            }
        }
    },
    plugins: [
    ]
}
