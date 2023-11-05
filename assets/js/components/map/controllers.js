import { Controller } from '@hotwired/stimulus'

import Point from './point.js'
import { DEFAULT_ZOOM, FOCUS_ZOOM, CITY_ZOOM, mapInit, addPoints, calculateBounds, addDraggableMarker } from './lib'
import { elementOnScreen, debounce } from '../../utils'

// TODO: refactor
class BaseController extends Controller {
    static targets = ['map']
    static values = { apikey: String, styleurl: String, centerlat: Number, centerlon: Number }

    async _mapInit() {
        let map = await mapInit(this.apikeyValue, this.mapOptions)
        this.map = map
        return map
    }

    get zoom() {
        return DEFAULT_ZOOM
    }

    get mapOptions() {
        return {
            container: this.mapTarget,
            style: this.styleurlValue,
            center: this.center,
            zoom: this.zoom
        }
    }

    get center() {
        return {lat: this.centerlatValue, lon: this.centerlonValue}
    }
}

// TODO: rename?
export class MapController extends BaseController {
    static targets = ['point', 'marker', 'buttonRow']

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
                    edit: pt.querySelector('a.edit-link').href,
                    buttonsRow: pt.dataset.buttonsRowLink
                }
            })
        })

        this.pointsMap = new Map(this.points.map(p => [p.id, p]))

        this._mapInit().then(map => addPoints(map, this.points))
    }

    get mapOptions() {
        return Object.assign(super.mapOptions,  {bounds: calculateBounds(this.points)})
    }

    panTo(ev) {
        ev.preventDefault()
        let point = this.pointsMap.get(ev.target.closest('li').id)
        this.map.flyTo({ center: point, zoom: FOCUS_ZOOM })

        if (!elementOnScreen(this.mapTarget)) {
            this.mapTarget.scrollIntoView({behavior: "smooth"})
        }
    }

    markerTargetConnected(el) {
        const point = this.pointsMap.get(el.dataset.pointId)

        el.setAttribute('role', 'button')
        el.setAttribute('hx-get', point.links.buttonsRow)
        el.setAttribute('hx-target', '#buttons_row')

        htmx.process(el) // Needed for the HTMX attributes to work
    }

    activateMarker(_ev) {
        this.buttonRowTarget.classList.remove('active')
    }

    postActivateMarker() {
        this.buttonRowTarget.classList.add('active')
    }

    dismissButtonRow() {
        this.buttonRowTarget.classList.remove('active')
    }
}

export class MapPointerController extends BaseController {
    static targets = ['lat', 'lon']
    static values = { mode: String }

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

    setCoordinates(event) {
        let coordinatesSource = event.params.source

        let lat, lng
        if(coordinatesSource == 'map') {
            ({lat, lng} = this.map.getCenter())
        } else {
            ({lat, lng} = this.marker.getLngLat())
        }
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

    get zoom() {
        if(this.modeValue == 'point') { return FOCUS_ZOOM }
        else { return CITY_ZOOM }
    }

    get center() {
        let point = this.point
        if(point.lat) { return point }
        return super.center
    }

    async _loadMap() {
        const map = await this._mapInit()

        if (this.modeValue == 'point') {
            const marker = addDraggableMarker(map)
            marker.on('dragend', () => this.setCoordinates({params: {source: 'marker'}}) )
            this.marker = marker
        }

        if (this.modeValue == 'city') {
            map.on('dragend', () => this.setCoordinates({params: {source: 'map'}}))
            map.on('moveend', debounce(() => map.zoomTo(this.zoom), 2500))
        }
    }
}
