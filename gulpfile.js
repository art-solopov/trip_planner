const { src, dest, series, watch } = require('gulp')
const concat = require('gulp-concat')
const postcss = require('gulp-postcss')
const sass = require('gulp-sass')
const mergeStreams = require('merge-stream')

sass.compiler = require('node-sass');

const postcssPlugins = {
    fontFamilySystemUI: require('postcss-font-family-system-ui'),
    easyImport: require('postcss-easy-import'),
    nesting: require('postcss-nesting'),
    simpleVars: require('postcss-simple-vars'),
    each: require('postcss-each'),
    extend: require('postcss-extend')
}

function css() {
    let assets =  src(['assets/css/app.scss'])
	.pipe(sass().on('error', sass.logError))
        .pipe(postcss([
            postcssPlugins.easyImport(),
            // postcssPlugins.each({
	    // 	plugins: {
	    // 	    beforeEach: [postcssPlugins.simpleVars()]
	    // 	}
	    // }),
            postcssPlugins.nesting(),
            // postcssPlugins.extend(),
            // postcssPlugins.simpleVars(),
            postcssPlugins.fontFamilySystemUI()
        ]))

    return assets.pipe(concat('app.css'))
        .pipe(dest('trip_planner/static/css/'))
}

function js() {
    let mapScripts = src(['assets/js/map/**/*.js', 'assets/js/map.js']).pipe(concat('map.js'))
    let pointFormScripts = src(['assets/js/point_form/**/*.js', 'assets/js/point_form.js']).pipe(concat('point_form.js'))

    let assets = mergeStreams(mapScripts, pointFormScripts)

    return assets.pipe(dest('trip_planner/static/js'))
}

function watchAssets() {
    return watch(['assets/**/*.scss', 'assets/**/*.css', 'assets/**/*.js'], {ignoreInitial: false}, exports.default)
}

exports.css = css
exports.js = js

exports.default = series(css, js)
exports.watch = watchAssets
