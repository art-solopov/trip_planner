function init() {
    const formDialog = document.getElementById('form_dialog')
    formDialog.addEventListener('htmx:afterSettle', () => {
        // dialog.showModal()
        // Beer.css specific code
        ui("#" + formDialog.id)
    })

    document.addEventListener('click', (ev) => {
        let {target} = ev;

        if((target.tagName == 'A' || target.tagName == 'BUTTON') && target.formMethod == 'dialog') {
            ui(target.closest('dialog'))
        }
    })
}

export default {init}
