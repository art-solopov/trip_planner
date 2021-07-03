import { Controller } from 'stimulus'

export default class FlashController extends Controller {
    remove() {
        this.element.remove()
    }
}
