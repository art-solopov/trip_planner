import { Controller } from '@hotwired/stimulus'

import Point from './func/point.js'
import { FOCUS_ZOOM, mapInit, addDragableMarker } from './func/map.js'
import { elementOnScreen } from '../../utils'

// TODO: refactor
class BaseController extends Controller {
    _mapInit() {
        return mapInit(this.mapTarget, this.apikeyValue, this.styleurlValue, this.points, this.center)
            .then(map => { this.map = map })
    }

    get center() {
        return {lat: this.centerlatValue, lon: this.centerlonValue}
    }
}

BaseController.targets = ['map']
BaseController.values = { apikey: String, styleurl: String, centerlat: Number, centerlon: Number }

// TODO: rename?
export class MapController extends BaseController {
    connect() {
        this.points = this.pointTargets.map(pt => {
            let lat = Number(pt.dataset.lat),
                lon = Number(pt.dataset.lon)
            return new Point({
                lat: Number(pt.dataset.lat),
                lon: Number(pt.dataset.lon),
                category: pt.dataset.category,
                name: pt.querySelector('.item-name').innerText,
                id: pt.id
            })
        })

        this.pointsMap = new Map(this.points.map(p => [p.id, p]))

        this._mapInit()
    }

    panTo(ev) {
        ev.preventDefault()
        let point = this.pointsMap.get(ev.target.closest('li').id)
        this.map.flyTo({ center: point, zoom: FOCUS_ZOOM })

        if (!elementOnScreen(this.mapTarget)) {
            this.mapTarget.scrollIntoView({behavior: "smooth"})
        }
    }
}

MapController.targets = [...BaseController.targets, 'point']
MapController.values = {...BaseController.values}

export class MapPointerController extends BaseController {
    get points() { return [] }

    connect() {
        window.mpctr = this // TODO debug
    }

    mapTargetConnected(e) {
        console.log('Got map target', e)
    }

    loadMap() {
        this._mapInit().then(map => addDragableMarker(map)).then(marker => this.marker = marker)
    }
}

MapPointerController.targets = [...BaseController.targets]
MapPointerController.values = {...BaseController.values}
