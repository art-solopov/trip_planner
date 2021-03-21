import { Application } from 'stimulus'

import MapController from './controllers/map_controller'

const app = Application.start()
app.register('map', MapController)
