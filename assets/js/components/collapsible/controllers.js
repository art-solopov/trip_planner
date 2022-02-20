import { Controller } from 'stimulus'

export default class CollapsibleController extends Controller {
    static targets = ['button']
    static classes = ['collapsed']

    toggle() {
        this.element.classList.toggle(this.collapsedClass)
        this._changeButton()
    }

    connect() {
        this._changeButton()
    }

    _changeButton() {
        let txt = ""
        if (this.element.classList.contains(this.collapsedClass)) {
            txt = "▶"
        } else {
            txt = "▼"
        }
        this.buttonTarget.innerText = txt
    }
}
