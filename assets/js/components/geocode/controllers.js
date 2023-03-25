import { Controller } from '@hotwired/stimulus'

export class GeocodeController extends Controller {
    setData(ev) {
        let result = ev.target.closest('.result')
        this.latTarget.value = result.dataset.lat
        this.lonTarget.value = result.dataset.lon
        result.dispatchEvent(new Event('geocode:set', {bubbles: true}))
    }
}

GeocodeController.targets = ['lat', 'lon', 'name', 'address', 'geocodeField', 'results']
