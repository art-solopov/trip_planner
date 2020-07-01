let currentInput = undefined;

class Row {
    constructor(rowEl) {
        this.el = rowEl
        this.openFrom = this.el.querySelector('input[name$=open_from]')
        this.openTo = this.el.querySelector('input[name$=open_to]')
    }

    static fromInput(input) {
        return new Row(input.closest('tr'))
    }

    static fromCurrent() {
        return Row.fromInput(currentInput)
    }

    data() {
        return {
            openFrom: this.openFrom.value,
            openTo: this.openTo.value
        }
    }

    setData({openFrom, openTo}) {
        this.openFrom.value = openFrom
        this.openTo.value = openTo
    }
}

export default function main() {
    const scheduleButtons = document.getElementById('schedule_buttons')
    scheduleButtons.classList.remove('mui--hide')
    const copyDownButton = scheduleButtons.querySelector('.btn-copy-down')
    const copyAllButton = scheduleButtons.querySelector('.btn-copy-all')

    let scheduleTable = document.getElementById('schedule')
    scheduleTable.addEventListener('focusin', event => {
        currentInput = event.target
        scheduleButtons.style.top = currentInput.offsetParent.offsetTop + 'px'
    })

    copyDownButton.addEventListener('click', () => {
        let row = Row.fromCurrent()
        let nextRowEl = row.el.nextElementSibling
        if (!nextRowEl) return;

        let nextRow = new Row(nextRowEl)
        nextRow.setData(row.data())
        nextRow.openFrom.focus()
    })

    copyAllButton.addEventListener('click', () => {
        let row = Row.fromCurrent()
        let data = row.data()

        let rowEls = scheduleTable.querySelectorAll('tbody tr')
        for (let el of rowEls) {
            let row = new Row(el)
            row.setData(data)
        }
    })
}
