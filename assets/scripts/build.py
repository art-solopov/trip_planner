from dataclasses import dataclass
from os.path import join as pjoin, splitext, basename
from os import makedirs
import subprocess as sp
import json

CSS_ENTRYPOINTS = ['app.scss']


@dataclass
class Asset:
    name: str
    src_path: str
    asset_name: str | None = None
    dest_path: str | None = None

    @property
    def dest_name(self):
        return basename(self.dest_path)


def build_css(outdir):
    assets = [Asset(name=e, src_path=pjoin('assets', 'css', e))
              for e in CSS_ENTRYPOINTS]

    for ep in assets:
        sass_sp = sp.run(['yarn', 'node', 'assets/scripts/compile-sass.js', ep.src_path], stdout=sp.PIPE)
        sass_out = sass_sp.stdout

        postcss_sp = sp.run(['yarn', 'run', 'postcss'], input=sass_out, stdout=sp.PIPE)
        postcss_out = postcss_sp.stdout

        fn, _ext = splitext(ep.name)
        ep.asset_name = f'{fn}.css'
        # TODO: add hashing
        ep.dest_path = pjoin(outdir, f'{fn}.css')
        with open(ep.dest_path, 'wb') as cssf:
            cssf.write(postcss_out)

    return assets


def main(static_folder):
    outdir = pjoin(static_folder, 'assets')
    makedirs(outdir, exist_ok=True)

    manifest = {}

    css_assets = build_css(outdir)
    for asset in css_assets:
        print(f"{asset.name} => {asset.dest_path}")  # TODO: replace with proper logging
        manifest[asset.asset_name] = asset.dest_name

    # TODO: deduplicate manifest path
    with open(pjoin(static_folder, 'assets', 'manifest.json'), 'w') as mf:
        json.dump(manifest, mf)


if __name__ == "__main__":
    from sys import argv
    _script_name, static_folder = argv
    main(static_folder)
