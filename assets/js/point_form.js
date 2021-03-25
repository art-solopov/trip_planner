// import geocodeMain from './PointForm/PointForm__Geocode.bs.js';
// import scheduleMain from './PointForm/PointForm__Schedule.bs.js';

import { Application } from 'stimulus'

import GeocodeController from './controllers/geocode_controller'

const app = Application.start()
app.register('geocode', GeocodeController)
