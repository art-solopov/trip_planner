const process = require('node:process')
const fs = require('node:fs/promises')
const path = require('node:path')
const {createHash} = require('node:crypto')
const {pathToFileURL} = require('node:url');

const sass = require('sass')
const postcss = require('postcss')
const esbuild = require('esbuild')

const bsImporter = {
    findFileUrl(url) {
        if(!url.startsWith('~bootstrap')) return null;
        return pathToFileURL(url.replace(/^~bootstrap/, 'assets/vendor/bootstrap/'))
    }
}

const postcssPlugins = [ 
    require('postcss-easy-import'),
    require('postcss-nesting'),
    require('postcss-font-family-system-ui'),
    require('autoprefixer')
]

const cssEntrypoint = 'assets/css/app.scss'
const jsEntrypoints = ['app', 'trip_form', 'trip_show', 'point_form'].map(e => `assets/js/${e}.js`)

function isProd() {
    return process.env.NODE_ENV === 'production'
}

async function css(outdir) {
    let res = sass.compile(cssEntrypoint, {importers: [bsImporter]})
    res = await postcss(postcssPlugins).process(res.css, {from: cssEntrypoint, to: 'app.css'})
    let outname = 'app.css'
    if(isProd()) {
        let h = createHash('md5').update(res.css).digest('base64')
        outname = `app-${h.substring(0, 8)}.css`
    }
    let outpath = path.join(outdir, outname)
    await fs.writeFile(outpath, res.css)
    return [{src: 'app.css', dest: outpath}]
}

async function js(outdir) {
    let result = await esbuild.build({
        entryPoints: jsEntrypoints,
        entryNames: isProd() ? '[name]-[hash]' : '[name]',
        assetNames: '[ext]/[name]-[hash]',
        bundle: true,
        write: false,
        splitting: true,
        metafile: true,
        minify: isProd(),
        publicPath: '/static/assets', // TODO: maybe inject from outside
        format: 'esm',
        alias: {
            bootstrap: './assets/vendor/bootstrap'
        },
        loader: {
            '.svg': 'file'
        },
        outdir
    })

    let outputFiles = result.outputFiles.map(async ofile => {
        await fs.mkdir(path.dirname(ofile.path), {recursive: true})
        return await fs.writeFile(ofile.path, ofile.contents)
    })
    await Promise.all(outputFiles)

    let manifest = []
    Object.entries(result.metafile.outputs).forEach(([outpath, e]) => {
        if(e.entryPoint) {
            let src = path.basename(e.entryPoint)
            manifest.push({ src, dest: outpath })

            if(e.cssBundle) {
                manifest.push({ src: src + '.css', dest: e.cssBundle })
            }
        }

    })
    return manifest
}

async function main() {
    const [_node, _script, outdir, subpath, manifestPath] = process.argv
    await fs.mkdir(outdir, {recursive: true})
    let manifest = (await css(outdir)).concat(await js(outdir))
    let mfst = manifest.map(e => [e.src, `${subpath}/${path.basename(e.dest)}`])
    await fs.writeFile(manifestPath, JSON.stringify(Object.fromEntries(mfst)))
    return manifest
}

main().then((manifest) => {
    for (let e of manifest) {
        console.log(`${e.src} => ${e.dest}`)
    }
})
