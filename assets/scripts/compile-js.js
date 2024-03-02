const process = require('node:process')
const fs = require('node:fs/promises')
const path = require('node:path')

const esbuild = require('esbuild')

const entryPoints = ['app', 'trip_form', 'trip_show', 'point_form'].map(e => `assets/js/${e}.js`)

const [_node, _script, outdir] = process.argv
esbuild.build({
    entryPoints,
    entryNames: '[name]-[hash]',
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
            let epName = path.basename(e.entryPoint)
            let assetName = path.basename(outpath)
            manifest.push({
                name: epName, src_path: e.entryPoint,
                asset_name: assetName, dest_path: outpath // TODO: fix after hashing is implemented
            })

            if(e.cssBundle) {
                manifest.push({
                    name: epName, src_path: e.entryPoint,
                    asset_name: path.basename(e.cssBundle), dest_path: e.cssBundle
                })
            }
        }
    })
    await Promise.all(outputFiles)
    console.log(result.metafile.outputs)
    return manifest
}).then((manifest) => process.stdout.write(JSON.stringify(manifest)))
