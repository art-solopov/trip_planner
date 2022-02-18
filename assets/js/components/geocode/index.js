// require('htmx.org')
import 'htmx.org/dist/htmx.js'

import { GeocodeController } from './controllers.js'

export default {
    controllers: [['geocode', GeocodeController]]
}
