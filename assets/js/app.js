import Dialog from './components/dialog'
import Tooltip from './components/tooltip'
import RepeatableField from './components/repeatable_field'
import Flash from './components/flash'

import {createApp} from "./init/stimulus";
import Alpine from "./init/alpine";

createApp(Dialog, Tooltip, RepeatableField)

Alpine.data('flash', Flash)

document.addEventListener('DOMContentLoaded', () => {
    Alpine.start()
})