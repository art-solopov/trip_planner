import { Controller } from '@hotwired/stimulus'

export class FlashController extends Controller {
    close() {
        // TODO: add animation
        this.element.remove()
    }
}
