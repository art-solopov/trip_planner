require('htmx.org')
import { Application } from 'stimulus'

import GeocodeController from './controllers/geocode_controller'
import PointFormScheduleController from './controllers/point_form_schedule_controller'

const app = Application.start()
app.register('geocode', GeocodeController)
app.register('point-form-schedule', PointFormScheduleController)
