import process from 'process'

import replace from '@rollup/plugin-replace';
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json'
import manifest from 'rollup-plugin-output-manifest'
import styles from 'rollup-plugin-styles'
import { terser } from 'rollup-plugin-terser'

const isProd = (process.env.NODE_ENV == 'production')

const COMPONENT_REGEXP = /components\/([a-z_]+)/

let outputConfig = {
    dir: 'trip_planner/static/assets',
    assetFileNames: '[name][extname]',
    format: 'es',
    sourcemap: true
}

if (isProd) {
    outputConfig.entryFileNames = '[name]-[hash].js'
    outputConfig.assetFileNames = '[name]-[hash][extname]'
}

export default {
    input: {
        point_form: 'assets/js/point_form.js',
        trip_show: 'assets/js/trip_show.js',
        trip_form: 'assets/js/trip_form.js',
        app: 'assets/js/app.js',
    },
    output: outputConfig,
    manualChunks(id, { getModuleInfo }) {
        if (id.includes('node_modules')) {
            if (isProd) return 'vendor';
            let comp_match = /node_modules(\/@[a-z_]+)?\/([a-z_]+)/.exec(id)
            return `node_modules/${comp_match[1] || ''}/${comp_match[2]}`
        }
        let comp_match = COMPONENT_REGEXP.exec(id)
        if (comp_match) {
            let modinfo = getModuleInfo(id)
            if (modinfo.importers.length + modinfo.dynamicImporters.length > 1) {
                console.log(`${id} => ${comp_match[1]}`)
                return comp_match[1]
            }
        }
    },
    plugins: [
        replace({
            'process.env.NODE_ENV': JSON.stringify('production')
        }),
        resolve({ jsnext: true, preferBuiltins: true, browser: true }),
        commonjs(),
        json(),
        styles({ mode: 'extract' }),
        isProd && terser(),
        manifest({ nameWithExt: false, publicPath: 'assets/' }),
    ]
};
