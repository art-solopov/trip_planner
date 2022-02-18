export default class Point {
    constructor({id, name, category, lat, lon}) {
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
