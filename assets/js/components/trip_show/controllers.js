import { Controller } from '@hotwired/stimulus'

export class TripShowController extends Controller {
    static targets = ['dataDrawer']

    showDataDrawer() {
        if(!this.dataDrawerTarget.open) {
            ui(this.dataDrawerTarget)
        }
    }
}
