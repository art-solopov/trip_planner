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

function watchAssets() {
    return watch(['assets/**/*.scss', 'assets/**/*.css'], {ignoreInitial: false}, exports.default)
}

exports.default = css
exports.watch = watchAssets
