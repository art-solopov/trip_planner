import { Controller } from 'stimulus'

class GeocodeController extends Controller {
    setData(ev) {
        let result = ev.target.closest('.geocode-result')
        this.latTarget.value = result.dataset.lat
        this.lonTarget.value = result.dataset.lon
    }

    _displayGeocode(data) {
        this.resultsTarget.innerHTML = ""
        if (data.length == 0) {
            this.resultsTarget.innerHTML = '<span class="text-error">No geocode results found</span>'
        } else {
            let template = document.getElementById('geocode_result_template')

            for (let d of data) {
                let el = document.importNode(template.content, true).querySelector('div')
                el.dataset.lat = d.lat
                el.dataset.lon = d.lon
                el.querySelector('.address').textContent = d.address
                el.querySelector('.name').textContent = d.name
                el.querySelector('.preview').src = d.map_url

                this.resultsTarget.appendChild(el)
            }
        }
    }
}

GeocodeController.targets = ['lat', 'lon', 'name', 'address', 'geocodeField', 'results']

export default GeocodeController
