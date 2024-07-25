import { Controller } from '@hotwired/stimulus'

function replaceVal(s, num) {
    // Positive lookbehind on '-'
    return s.replace(/(?<=-)\d+$/, num)
}

export class RepeatableFieldController extends Controller {
    static targets = ['control', 'removeButton', 'addButton']
    static values = {
        count: Number,
        maxEntries: Number
    }

    addField() {
        let control = this.controlTargets[0].cloneNode(true)
        let removeButton = this.removeButtonTargets[0].cloneNode(true)
        let controlInput = control.querySelector('input')
        const count = this.countValue + 1

        controlInput.id = replaceVal(controlInput.id, count)
        controlInput.name = replaceVal(controlInput.name, count)
        controlInput.value = ''
        removeButton.dataset.targetId = replaceVal(removeButton.dataset.targetId, count)

        this.addButtonTarget.insertAdjacentElement('beforebegin', control)
        this.addButtonTarget.insertAdjacentElement('beforebegin', removeButton)
        this.countValue = count
        this._toggleAddButton()
    }

    removeField(event) {
        const removeButton = event.target.closest('button')
        const control = this.controlTargets.find(e => e.id === removeButton.dataset.targetId)
        
        control.remove()
        removeButton.remove()
        this._toggleAddButton()
    }

    _toggleAddButton() {
        this.addButtonTarget.disabled = this.countValue >= this.maxEntriesValue
    }
}
