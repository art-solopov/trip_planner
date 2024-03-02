const process = require('node:process')
const fs = require('node:fs/promises')
const path = require('node:path')

const esbuild = require('esbuild')

const entryPoints = ['app', 'trip_form', 'trip_show', 'point_form'].map(e => `assets/js/${e}.js`)

const [_node, _script, outdir] = process.argv
esbuild.build({
    entryPoints,
    bundle: true,
    write: false,
    splitting: true,
    metafile: true,
    format: 'esm',
    loader: {
        '.svg': 'file'
    },
    outdir
}).then(async result => {
    let manifest = []
    let outputFiles = result.outputFiles.map(ofile => fs.writeFile(ofile.path, ofile.contents))
    Object.entries(result.metafile.outputs).forEach(([outpath, e]) => {
        if(!!e.entryPoint) {
            // manifest[path.basename(e.entryPoint)] = path.basename(outpath)
            manifest.push({
                name: path.basename(e.entryPoint), src_path: e.entryPoint,
                asset_name: path.basename(outpath), dest_path: outpath // TODO: fix after hashing is implemented
            })
        }
    })
    await Promise.all(outputFiles)
    return manifest
}).then((manifest) => process.stdout.write(JSON.stringify(manifest)))
