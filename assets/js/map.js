import createApp from './utils/create_app'

import MapController from './controllers/map_controller'

const app = createApp([['map', MapController]])

initAddPointButton()
