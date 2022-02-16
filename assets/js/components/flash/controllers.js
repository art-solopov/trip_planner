import { Controller } from 'stimulus'

export class FlashController extends Controller {
    remove() {
        this.element.remove()
    }
}
