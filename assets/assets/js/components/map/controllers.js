import { Controller } from '@hotwired/stimulus'

import { Point, loadFromScript } from './func/point.js'
import { DEFAULT_ZOOM, FOCUS_ZOOM, mapInit, calculateBounds, addDraggableMarker } from './func/map.js'
import { elementOnScreen } from '../../utils'

// TODO: refactor
class BaseController extends Controller {
    static zoom = DEFAULT_ZOOM

    async _mapInit() {
        let map = await mapInit(this.apikeyValue, this.mapOptions)
        this.map = map
        return map
    }

    get mapOptions() {
        return {
            container: this.mapTarget,
            style: this.styleurlValue,
            center: this.center,
            zoom: this.constructor.zoom
        }
    }

    get center() {
        return { lat: this.centerlatValue, lon: this.centerlonValue }
    }
}

BaseController.targets = ['map']
BaseController.values = { apikey: String, styleurl: String, centerlat: Number, centerlon: Number }

export class CityMapController extends BaseController {
    connect() {
        const points = loadFromScript(this.dataScriptIdValue)
        this.bounds = calculateBounds(points)
        this.points = new Map(points.map(p => [p.id, p]))
        this._mapInit()
    }

    get mapOptions() {
        return { ...super.mapOptions, bounds: this.bounds }
    }

    panTo(ev) {
        ev.preventDefault()
        let point = this.points.get(ev.target.closest('li').dataset.slug)
        this.map.flyTo({ center: point, zoom: FOCUS_ZOOM })

        if (!elementOnScreen(this.mapTarget)) {
            this.mapTarget.scrollIntoView({ behavior: "smooth" })
        }
    }
}

CityMapController.targets = [...BaseController.targets]
CityMapController.values = { ...BaseController.values, dataScriptId: String }
