import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json'
import manifest from 'rollup-plugin-output-manifest'
import styles from 'rollup-plugin-styles'

export default {
    input: {
        point_form: 'assets/js/point_form.js',
        map: 'assets/js/map.js',
        app: 'assets/js/app.js',
    },
    output: {
        dir: 'trip_planner/static/assets',
        entryFileNames: '[name]-[hash].js',
        assetFileNames: '[name]-[hash][extname]',
        format: 'es',
        sourcemap: true
    },
    manualChunks(id, {getModuleInfo}) {
        if(id.includes('node_modules')) { return 'vendor' }
    },
    plugins: [
        resolve({jsnext: true, preferBuiltins: true, browser: true}),
        commonjs(),
        json(),
        styles({mode: 'extract'}),
        manifest({nameWithExt: false, publicPath: 'assets/'}),
    ]
};
