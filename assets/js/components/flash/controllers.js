import { Controller } from '@hotwired/stimulus'

export class FlashController extends Controller {
    remove() {
        this.element.remove()
    }
}
