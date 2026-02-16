import { Controller } from '@hotwired/stimulus'

export class TripShowController extends Controller {
    static targets = ['dataDrawer']

    showDataDrawer() {
        ui(this.dataDrawerTarget)
    }
}
