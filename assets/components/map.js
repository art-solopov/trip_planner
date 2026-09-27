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
                .map(e => e.dataset)

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

            const map = new mapboxgl.Map(mapOptions)
           
            for(let point of points) {
                let marker = new mapboxgl.Marker()
                    .setLngLat([point.lon, point.lat])
                    .addTo(map)
            }
        }
    }
}
