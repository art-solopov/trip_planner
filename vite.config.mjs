import { defineConfig } from 'vite'

export default defineConfig({
  root: 'assets',
  input: ['js/app.js',
    'js/point_form.js',
    'js/trip_form.js',
    'js/trip_show.js',
    'css/app.scss',
    'css/vars.css'],
  build: {
    outDir: '../trip_planner/static',
    manifest: 'vite.manifest.json'
  }
})
