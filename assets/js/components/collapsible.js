import { Controller } from '@hotwired/stimulus'

class CollapsibleController extends Controller {
    toggle() {
        // TODO: add animations
        this.element.classList.toggle('open')
        this.element.dispatchEvent(new Event('collapsible.toggled'))

        const eventName = this.element.classList.contains('open') ? 'collapsible.opened' : 'collapsible.closed'
        this.element.dispatchEvent(new Event(eventName))
    }
}

export default {
    controllers: [['collapsible', CollapsibleController]]
}
