const containerId = 'add_point_form_container'
const buttonId = 'add_point_with_url_button'
const hiddenClass = 'hidden'

export function initAddPointButton() {
    let button = document.getElementById(buttonId)
    let container = document.getElementById(containerId)
    button.addEventListener('click', (ev) => {
        ev.preventDefault()
        container.classList.toggle(hiddenClass)
        if(!container.classList.contains(hiddenClass)) {
            container.querySelector('input[type=text]').focus()
        }
    })

    document.body.addEventListener('click', ev => {
        let { target } = ev
        if(target.closest(`#${buttonId}`) == null && target.closest(`#${containerId}`) == null) {
            container.classList.add(hiddenClass)
        }
    })
}
