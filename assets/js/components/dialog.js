function init() {
    const dialog = document.getElementById('form_dialog')
    dialog.addEventListener('htmx:afterSettle', () => { dialog.showModal() })
    dialog.addEventListener('click', (ev) => {
        if(ev.target == dialog) { dialog.close() }
    })
}

export default {init}
