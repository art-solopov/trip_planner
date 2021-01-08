const { src, dest, series, watch } = require('gulp')
const concat = require('gulp-concat')
const postcss = require('gulp-postcss')
const mergeStreams = require('merge-stream')
const webpackStream = require('webpack-stream')

const webpackConfig = require('./webpack.config.js')

webpackConfig.mode = 'production'

// const postcssPlugins = {
//     fontFamilySystemUI: require('postcss-font-family-system-ui'),
//     easyImport: require('postcss-easy-import'),
//     nesting: require('postcss-nesting'),
//     simpleVars: require('postcss-simple-vars'),
//     each: require('postcss-each'),
//     extend: require('postcss-extend'),
//     tailwindcss: require('tailwindcss')
// }

function css() {
    let assets =  src(['assets/css/app.css'])
        .pipe(postcss())

    return assets.pipe(concat('app.css'))
        .pipe(dest('trip_planner/static/css/'))
}

function webpackProd() {
    return webpackStream(webpackConfig)
        .pipe(dest(webpackConfig.output.path))
}

function watchAssets() {
    return watch(['assets/**/*.css'], {ignoreInitial: false}, css)
}

exports.css = css
exports['webpack-prod'] = webpackProd
exports.watch = watchAssets
