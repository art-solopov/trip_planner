import { makeMarker } from "./marker"

export default function(centerLat, centerLon) {
    return {
        init() {
            let {mapApiKey, mapStyleUrl} = this.$el.dataset
            let mapOptions = {
                accessToken: mapApiKey,
                container: this.$refs.map,
                style: mapStyleUrl,
            }

            const points = [...this.$refs.pointsList.querySelectorAll('li')]
                .map(e => Object.assign({}, e.dataset, {marker: makeMarker(e)}))

            if(points.length > 1) {
                mapOptions.bounds = [
                    Math.min(...points.map(e => e.lon)),
                    Math.min(...points.map(e => e.lat)),
                    Math.max(...points.map(e => e.lon)),
                    Math.max(...points.map(e => e.lat))
                ]
            } else {
                mapOptions.center = [centerLon, centerLat]
                mapOptions.zoom = 12
            }

            this.map = new mapboxgl.Map(mapOptions)
           
            for(let point of points) {
                let marker = new mapboxgl.Marker({element: point.marker, anchor: 'bottom'})
                    .setLngLat([point.lon, point.lat])
                    .addTo(this.map)
            }
        }
    }
}
