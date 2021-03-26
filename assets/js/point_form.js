import { Application } from 'stimulus'

import GeocodeController from './controllers/geocode_controller'

const app = Application.start()
app.register('geocode', GeocodeController)

