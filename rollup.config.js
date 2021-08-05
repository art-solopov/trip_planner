import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json'
import manifest from 'rollup-plugin-output-manifest'
import styles from 'rollup-plugin-styles'

export default {
    input: {
        point_form: 'assets/js/point_form.js',
        map: 'assets/js/map.js',
        shared_app: 'assets/js/shared_app.js',
        app: 'assets/css/app.css'
    },
    output: {
        dir: 'trip_planner/static/js',
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
        // postcss({extract: path.resolve('trip_planner/static/css/app-[hash].css')}),
        styles({mode: 'extract'}),
        manifest({nameWithExt: false}),
    ]
};
