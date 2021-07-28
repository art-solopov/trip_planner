const { src, dest, series, watch } = require('gulp')
const concat = require('gulp-concat')
const postcss = require('gulp-postcss')

function css() {
    let assets =  src(['assets/css/app.css'])
        .pipe(postcss())

    return assets.pipe(concat('app.css'))
        .pipe(dest('trip_planner/static/css/'))
}

function watchAssets() {
    return watch(['assets/**/*.css'], {ignoreInitial: false}, css)
}

exports.css = css
exports.watch = watchAssets
