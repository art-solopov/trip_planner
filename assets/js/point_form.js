// require('htmx.org')
import 'htmx.org/dist/htmx.js'

import createApp from './utils/create_app'

import GeocodeController from './controllers/geocode_controller'
import PointFormScheduleController from './controllers/point_form_schedule_controller'

const app = createApp([['geocode', GeocodeController], ['point-form-schedule', PointFormScheduleController]])
