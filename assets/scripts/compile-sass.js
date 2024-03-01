const process = require('node:process')
const {pathToFileURL} = require('node:url');

const sass = require('sass')

const bsImporter = {
    findFileUrl(url) {
        if(!url.startsWith('~bootstrap')) return null;
        return pathToFileURL(url.replace(/^~bootstrap/, 'assets/vendor/bootstrap/'))
    }
}

const [_node, _script, endpoint] = process.argv

const res = sass.compile(endpoint, {importers: [bsImporter]})
process.stdout.write(res.css)

