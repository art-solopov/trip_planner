export class Point {
    constructor({ id, name, category, lat, lon }) {
        this.id = id
        this.name = name
        this.category = category
        this.lat = lat
        this.lon = lon
    }

    toGeoJsonFeature() {
        return {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [this.lon, this.lat]
            },
            properties: {
                name: this.name,
                ptid: this.id,
                category: this.category
            }
        }
    }
}

export function loadFromScript(script_id) {
    const scriptData = JSON.parse(document.getElementById(script_id).innerText)
    return scriptData.map(pt => {
        let lat = Number(pt.lat),
            lon = Number(pt.lon)
        return new Point({
            ...pt,
            lat,
            lon,
            id: pt.slug
        })
    })
}
