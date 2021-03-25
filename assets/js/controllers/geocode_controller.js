import { Controller } from 'stimulus'
import axios from 'axios'

class GeocodeController extends Controller {
    geocode(_ev) {
        let tripId = this.element.dataset.tripId
        let name = this.nameTarget.value
        let address = this.addressTarget.value
        let field = this.geocodeFieldTargets.find(el => el.checked).value

        let data = {"trip_id": tripId, name, address, field}
        axios.post('/api/geocode', data).then(response => {
            let data = response.data
            this._displayGeocode(data)
        })
    }

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
