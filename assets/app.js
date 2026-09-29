import './app.scss'

import Alpine from 'alpinejs'
import.meta.glob('./pages/*.js', {eager: true})

window.Alpine = Alpine
Alpine.start()
