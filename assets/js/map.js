import createApp from './utils/create_app'

import MapController from './controllers/map_controller'

import { initAddPointButton } from './trip_show/trip_show.js'

const app = createApp([['map', MapController]])

initAddPointButton()
