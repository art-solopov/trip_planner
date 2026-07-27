import { defineConfig } from 'vite'

export default defineConfig(({ command }) => {
    return {
        root: 'assets',
        build: {
            manifest: true,
            base: '/assets/',
            outDir: 'trip_planner/static',
            rolldownOptions: {
                input: ['app.js']
            }
        },
        server: {
            strictPort: true,
            base: '/'
        }
    }
})
