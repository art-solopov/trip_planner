import { Controller } from 'stimulus'

import Point from './func/point.js'
import { FOCUS_ZOOM, mapInit } from './func/map.js'

function elementOnScreen(element) {
    let rect = element.getBoundingClientRect()
    return rect.top >= 0 && rect.top <= window.innerHeight && rect.bottom >= 0
}

export class MapController extends Controller {
    connect() {
        let points = this.pointTargets.map(pt => {
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

        this.points = new Map(points.map(p => [p.id, p]))

        let lats = points.map(p => p.lat)
        let lons = points.map(p => p.lon)

        let bounds = [
            { lon: Math.min(...lons), lat: Math.min(...lats) },
            { lon: Math.max(...lons), lat: Math.max(...lats) }
        ]

        mapInit(this.mapTarget, this.apikeyValue, this.styleurlValue, points, bounds)
            .then(map => this.map = map)
    }

    panTo(ev) {
        ev.preventDefault()
        let point = this.points.get(ev.target.closest('li').id)
        this.map.flyTo({ center: point, zoom: FOCUS_ZOOM })

        if (!elementOnScreen(this.mapTarget)) {
            this.mapTarget.scrollIntoView({behavior: "smooth"})
        }
    }
}

MapController.targets = ['point', 'map']
MapController.values = { apikey: String, styleurl: String }
