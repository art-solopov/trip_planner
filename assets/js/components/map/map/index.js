import {iconsUrl} from '../../../utils'

import MoveMarkerControl from './move-marker-control'

import styles from './marker-styles.module.scss'

export const DEFAULT_ZOOM = 10
export const CITY_ZOOM = 11.5
export const FOCUS_ZOOM = 15.0
const FIT_BOUND_OPTIONS = {
    padding: 32,
    maxZoom: FOCUS_ZOOM
}

// TODO: maybe inject from backend
const ICONS = {
    museum: 'easel',
    sight: 'star',
    transport: 'train-front',
    accomodation: 'house',
    food: 'cup-hot',
    entertainment: 'dpad',
    shop: 'basket3',
    other: 'pentagon'
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

            resolve(map)
        })
    })
}

function addPointsMarkers(map, points) {
    for (let point of points) {
        const el = document.createElement('div')
        el.className = `${styles.marker} ${styles[point.category]}`
        const icon = ICONS[point.category]

        el.innerHTML = `
            <svg class=${styles.markerBody}><use xlink:href="${iconsUrl}#geo-alt-fill"></svg>
            <svg class=${styles.markerIcon}><use xlink:href="${iconsUrl}#${icon}-fill"></svg>
        `

        const popup = new mapboxgl.Popup({
            offset: [0, -20]
        }).setHTML(`
            <p>${point.name}</p>
            <p>
                <a href="${point.links.more}">More</a>
                <a href="${point.links.edit}">Edit</a>
            </p>
            `)

        new mapboxgl.Marker({
            anchor: 'bottom',
            element: el
        }).setLngLat(point)
            .setPopup(popup)
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
