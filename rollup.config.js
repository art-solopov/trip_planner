import process from 'process'

import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json'
import manifest from 'rollup-plugin-output-manifest'
import styles from 'rollup-plugin-styles'
import { terser } from 'rollup-plugin-terser'

const isProd = (process.env.NODE_ENV == 'production')

const COMPONENT_REGEXP = /components\/([a-z_]+)/

let outputConfig = {
    dir: 'assets/static',
    assetFileNames: '[name][extname]',
    format: 'es',
    sourcemap: true
}

if(isProd) {
    outputConfig.entryFileNames = '[name]-[hash].js'
    outputConfig.assetFileNames = '[name]-[hash][extname]'
}

export default {
    input: {
        // point_form: 'assets/js/point_form.js',
        // trip_show: 'assets/js/trip_show.js',
        // trip_form: 'assets/js/trip_form.js',
        app: 'assets/assets/js/app.js',
        locations: 'assets/assets/js/locations.js'
    },
    output: outputConfig,
    manualChunks(id, {getModuleInfo}) {
        if(id.includes('node_modules')) { return 'vendor' }
        let comp_match = COMPONENT_REGEXP.exec(id)
        if(comp_match) {
            let modinfo = getModuleInfo(id)
            if (modinfo.importers.length + modinfo.dynamicImporters.length > 1) {
                console.log(`${id} => ${comp_match[1]}`)
                return comp_match[1]
            }
        }
    },
    plugins: [
        resolve({jsnext: true, preferBuiltins: true, browser: true}),
        commonjs(),
        json(),
        styles({mode: 'extract'}),
        isProd && terser(),
        manifest({nameWithExt: false, publicPath: '/static/'}),
    ]
};
