import styles from './marker-styles.module.scss'

export const DEFAULT_ZOOM = 10
export const FOCUS_ZOOM = 15.0
const FIT_BOUND_OPTIONS = {
    padding: 32,
    maxZoom: FOCUS_ZOOM
}

export async function mapInit(apiKey, points, options) {
    mapboxgl.accessToken = apiKey
    console.log(styles)

    options.bounds = calculateBounds(points)
    const map = await loadMap(options)
    addPointsLayer(map, points)
    addPointsMarkers(map, points)

    return map;
}

export function addDraggableMarker(map) {
    const marker = new mapboxgl.Marker({anchor: 'bottom', draggable: true})
    marker.setLngLat(map.getCenter()).addTo(map)
    return marker
}

function calculateBounds(points) {
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

function addImages(map, points) {
    const categories = new Set(points.map(pt => pt.category))
    const promises = [];
    for (let ct of categories) {
        let ctt = ct
        let promise = new Promise((resolve, reject) => {
            map.loadImage(`/static/icons/${ctt}.png`, (error, img) => {
                if(error) {
                    reject(error);
                    return
                }

                let imageId = `category:${ctt}`
                map.addImage(imageId, img);
                resolve(imageId)
            })
        })
        promises.push(promise)
    }

    return Promise.allSettled(promises)
}

function addPointsMarkers(map, points) {
    // import('./marker-styles.module.scss').then(mod => console.log(mod))

    for (let point of points) {
        const popup = new mapboxgl.Popup({
            offset: [0, -20]
        }).setText(point.name)
        const el = document.createElement('img')
        import(`./icons/${point.category}.png`).then(imgmod => el.src = imgmod.default)

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
