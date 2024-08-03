function init() {
    const dialog = document.getElementById('form_dialog')
    dialog.addEventListener('htmx:afterSettle', () => {
        // dialog.showModal()
        // Beer.css specific code
        ui("#" + dialog.id)
    })
    dialog.addEventListener('click', (ev) => {
        let {target} = ev;

        // if(target == dialog) { dialog.close() }
        // For Beer.css dialogs
        if((target.tagName == 'A' || target.tagName == 'BUTTON') && target.formMethod == 'dialog') {
            ui('#' + dialog.id)
        }
    })
}

export default {init}
