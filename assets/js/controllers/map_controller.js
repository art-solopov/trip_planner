import { Controller } from 'stimulus'

function elementOnScreen(element) {
    let rect = element.getBoundingClientRect()
    return rect.top >= 0 && rect.top <= window.innerHeight && rect.bottom >= 0
}

// const MapIcon = L.Icon.extend({
//     options: {
//         iconSize: [34, 51],
//         iconAnchor: [34 / 2, 51],
//         popupAnchor: [0, -30]
//     }
// })

class MapController extends Controller {
    connect() {
        let points = this.pointTargets.map(pt => {
            return {
                lat: Number(pt.dataset.lat),
                lon: Number(pt.dataset.lon),
                category: pt.dataset.category,
                name: pt.querySelector('.item-name').innerText,
                id: pt.id
            }
        })

        this.points = new Map(points.map(p => [p.id, p]))

        let lats = points.map(p => p.lat)
        let lons = points.map(p => p.lon)

        let bounds = [
            [Math.min(...lats), Math.min(...lons)],
            [Math.max(...lats), Math.max(...lons)]
        ]

        // this.map = L.map(this.mapTarget)
        // this.map.fitBounds(bounds)
        // L.tileLayer(this.urlValue, {attribution: this.attributionValue})
        //     .addTo(this.map)

        // for (var point of points) {
        //     let icon = new MapIcon({iconUrl: `/static/icons/${point.category}.png`})
        //     let marker = L.marker([point.lat, point.lon], {icon}).addTo(this.map)
        //     marker.bindPopup(point.name)
        // }
    }

    panTo(ev) {
        ev.preventDefault()
        let point = this.points.get(ev.target.closest('li').id)
        // this.map.panTo([point.lat, point.lon])

        // if (!elementOnScreen(this.mapTarget)) {
        //     this.mapTarget.scrollIntoView({behavior: "smooth"})
        // }
    }
}

MapController.targets = ['point', 'map']
MapController.values = { url: String, attribution: String }

export default MapController
