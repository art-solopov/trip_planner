import './app.scss'

import Alpine from 'alpinejs'

import map from './components/map'

Alpine.data('map', map)

window.Alpine = Alpine
Alpine.start()
