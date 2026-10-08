import { createApp } from './init/stimulus'

import Geocode from './components/geocode'
import PointForm from './components/point_form'
import Map from './components/map'

createApp(Geocode, PointForm, Map)
