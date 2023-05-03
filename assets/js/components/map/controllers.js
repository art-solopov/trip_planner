import { Controller } from '@hotwired/stimulus'

import Point from './func/point.js'
import { DEFAULT_ZOOM, FOCUS_ZOOM, mapInit, addDraggableMarker } from './func/map.js'
import { elementOnScreen } from '../../utils'

// TODO: refactor
class BaseController extends Controller {
    static zoom = DEFAULT_ZOOM

    _mapInit() {
        return mapInit(this.apikeyValue, this.points, this.mapOptions)
            .then(map => { this.map = map; return map })
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
                lat, lon,
                category: pt.dataset.category,
                name: pt.querySelector('.item-name').innerText,
                id: pt.id,
                links: {
                    more: pt.querySelector('a.more-link').href,
                    // edit: pt.querySelector('a.edit-link').href
                }
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
    static zoom = FOCUS_ZOOM

    get points() { return [] }

    mapTargetConnected(el) {
        let { centerLat, centerLon } = el.dataset
        if (centerLat != null && centerLon != null) {
            this.centerlatValue = centerLat
            this.centerlonValue = centerLon
        }
        this._loadMap()
    }

    moveMap() {
        if(this.map == null) return;
        this.map.easeTo({center: this.point})
        this.marker.setLngLat(this.point)
    }

    setCoordinates() {
        let {lat, lng} = this.marker.getLngLat()
        this.latTarget.value = lat
        this.lonTarget.value = lng
    }

    get lat() {
        return Number(this.latTarget.value)
    }

    get lon() {
        return Number(this.lonTarget.value)
    }

    get point() {
        return {lat: this.lat, lon: this.lon}
    }

    get center() {
        let point = this.point
        if(point.lat) { return point }
        return super.center
    }

    _loadMap() {
        this._mapInit()
            .then(map => addDraggableMarker(map))
            .then(marker => marker.on('dragend', this.setCoordinates.bind(this)))
            .then(marker => { this.marker = marker })
    }
}

MapPointerController.targets = [...BaseController.targets, 'lat', 'lon']
MapPointerController.values = {...BaseController.values}
