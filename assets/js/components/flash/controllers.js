import { Controller } from '@hotwired/stimulus'

export class FlashController extends Controller {
    close() {
        this.element.remove()
    }
}
