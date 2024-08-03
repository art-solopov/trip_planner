import {iconsUrl} from '../../../utils'

import MoveMarkerControl from './move-marker-control'

import styles from './marker-styles.module.css'
import icons from './icons'

export const DEFAULT_ZOOM = 10
export const CITY_ZOOM = 11.5
export const FOCUS_ZOOM = 15.0
const FIT_BOUND_OPTIONS = {
    padding: 32,
    maxZoom: FOCUS_ZOOM
}

export async function mapInit(apiKey, options) {
    mapboxgl.accessToken = apiKey

    const map = await loadMap(options)
    return map;
}

export function addPoints(map, points) {
    addPointsLayer(map, points)
    addPointsMarkers(map, points)
}

export function addDraggableMarker(map) {
    const marker = new mapboxgl.Marker({anchor: 'bottom', draggable: true})
    marker.setLngLat(map.getCenter()).addTo(map)

    map.addControl(new MoveMarkerControl(marker), 'bottom-right')

    return marker
}

export function calculateBounds(points) {
    if (points.length == 0) return undefined;

    let lats = points.map(p => p.lat)
    let lons = points.map(p => p.lon)
    return [
        { lon: Math.min(...lons), lat: Math.min(...lats) },
        { lon: Math.max(...lons), lat: Math.max(...lats) }
    ]
}

function loadMap(options) {
    const map = new mapboxgl.Map({
        ...options,
        fitBoundsOptions: FIT_BOUND_OPTIONS,
        attributionControl: true
    });

    return new Promise((resolve, _reject) => {
        map.on('load', () => {
            const nav = new mapboxgl.NavigationControl();
            map.addControl(nav, 'top-left');

            const sc = new mapboxgl.ScaleControl();
            map.addControl(sc);

            const glc = new mapboxgl.GeolocateControl();
            map.addControl(glc);

            map.on('click', (ev) => console.log(ev))

            resolve(map)
        })
    })
}

function addPointsMarkers(map, points) {
    for (let point of points) {
        const el = document.createElement('div')
        el.className = `${styles.marker} is-${point.category}`
        el.dataset.mapTarget = 'marker'
        el.dataset.action = 'click->map#activateMarker'
        el.dataset.pointId = point.id

        el.innerHTML = [
            `<svg class=${styles.markerBody}><use xlink:href="${iconsUrl}#marker" /></svg>`,
            `<img class=${styles.markerIcon} src=${icons[point.category]}></img>`
        ].join("\n")


        new mapboxgl.Marker({
            anchor: 'bottom',
            element: el
        }).setLngLat(point)
            .addTo(map)
    }
}

function addPointsLayer(map, points) {
    let data = {
        type: 'FeatureCollection',
        features: points.map(pt => pt.toGeoJsonFeature())
    }

    map.addSource('points', {type: 'geojson', data})
    map.addLayer({
        id: 'points',
        type: 'symbol',
        source: 'points',
        layout: {
            'text-anchor': 'top',
            'text-field': ['get', 'name'],
            'text-size': 14,
            'text-allow-overlap': true,
            'text-radial-offset': ['interpolate',
                ['linear'],
                ['zoom'],
                12, 0,
                14.4, 1.5
            ]
        }
    })
}
