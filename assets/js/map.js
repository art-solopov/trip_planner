import { Application } from 'stimulus'

import MapController from './controllers/map_controller'

import { initAddPointButton } from './trip_show/trip_show.js'

const app = Application.start()
app.register('map', MapController)

initAddPointButton()
