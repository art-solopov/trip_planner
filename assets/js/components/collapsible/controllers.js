import { Controller } from '@hotwired/stimulus'

const OPEN_EVENT = 'collapsible:open'
const CLOSED_EVENT = 'collapsible:closed'

export default class CollapsibleController extends Controller {
    static targets = ['button']
    static classes = ['collapsed']

    connect() {
        this._changeButton()
        this._emitEvent()
    }

    toggle() {
        this.element.classList.toggle(this.collapsedClass)
        this._changeButton()
        this._emitEvent()
    }

    get _isCollapsed() {
        return this.element.classList.contains(this.collapsedClass)
    }

    _emitEvent() {
        let eventName = this._isCollapsed ? CLOSED_EVENT : OPEN_EVENT
        this.element.dispatchEvent(new Event(eventName))
    }

    _changeButton() {
        let txt = this._isCollapsed ? "▶" : "▼"
        this.buttonTarget.querySelector('span').innerText = txt
    }
}
