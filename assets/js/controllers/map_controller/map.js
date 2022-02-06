export default async function mapInit(container, apiKey, style, points, bounds) {
    mapboxgl.accessToken = apiKey

    const map = await loadMap(container, style, bounds)
    let imgs = await addImages(map, points)
    addPointsLayer(map, points)

    return map;
}

function loadMap(container, style, bounds) {
    const map = new mapboxgl.Map({
        container, style, bounds,
        attributionControl: true
    });

    return new Promise((resolve, _reject) => {
        map.on('load', () => {
            const nav = new mapboxgl.NavigationControl();
            map.addControl(nav, 'top-left');

            const sc = new mapboxgl.ScaleControl();
            map.addControl(sc);
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
            'icon-image': ['concat', 'category:', ['get', 'category']],
            'icon-size': 0.5,
            'icon-anchor': 'bottom',
            'text-anchor': 'top',
            'text-field': ['get', 'name']
        }
    })
}
