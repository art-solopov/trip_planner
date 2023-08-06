import { Controller } from '@hotwired/stimulus'
import Tooltip from 'bootstrap/js/dist/tooltip';

export class BSTooltipController extends Controller {
    connect() {
        this.bstooltip = new Tooltip(this.element)
    }
}
