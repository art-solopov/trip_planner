import { Controller } from '@hotwired/stimulus'

function replaceVal(s, num) {
    // Positive lookbehind on '-'
    return s.replace(/(?<=-)\d+$/, num)
}

export class RepeatableFieldController extends Controller {
    static targets = ['control', 'removeButton', 'addButton']
    static values = {
        count: Number
    }

    addField() {
        let control = this.controlTargets[0].cloneNode()
        let removeButton = this.removeButtonTargets[0].cloneNode(true)
        const count = this.countValue + 1

        control.id = replaceVal(control.id, count)
        control.name = replaceVal(control.name, count)
        control.value = ''
        removeButton.dataset.targetId = replaceVal(removeButton.dataset.targetId, count)

        this.addButtonTarget.insertAdjacentElement('beforebegin', control)
        this.addButtonTarget.insertAdjacentElement('beforebegin', removeButton)
        this.countValue = count
    }

    removeField(event) {
        const removeButton = event.target.closest('button')
        const control = this.controlTargets.find(e => e.id === removeButton.dataset.targetId)
        
        control.remove()
        removeButton.remove()
    }
}
