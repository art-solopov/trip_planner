import { Controller } from '@hotwired/stimulus'

export class ScheduleController extends Controller {
    connect() {
        this.currentRow = null
    }

    shiftScheduleButtons(ev) {
        this.buttonsTarget.classList.remove('invisible')
        let currentRow = ev.target.closest('tr')
        this.currentRow = currentRow
        let offsetTop = currentRow.offsetTop + currentRow.closest('tbody').offsetTop
        this.buttonsTarget.style.top = `${offsetTop}px`
    }

    copyNext(_ev) {
        let nextRow = this.currentRow.nextElementSibling
        if(nextRow == null) return;

        this._copyData(this.currentRow, nextRow)
        this._rowInputs(nextRow).openFrom.focus()
    }

    copyAll(_ev) {
        let rows = this.currentRow.parentElement.querySelectorAll('tr')
        for (let row of rows) {
            if(row == this.currentRow) { continue; }
            this._copyData(this.currentRow, row)
        }
    }

    _rowInputs(row) {
        return {
            openFrom: row.querySelector('[name$=open_from]'),
            openTo: row.querySelector('[name$=open_to]')
        }
    }

    _copyData(fromRow, toRow) {
        let fromInputs = this._rowInputs(fromRow)
        let toInputs = this._rowInputs(toRow)

        toInputs.openFrom.value = fromInputs.openFrom.value
        toInputs.openTo.value = fromInputs.openTo.value
    }
}

ScheduleController.targets = ['buttons']
