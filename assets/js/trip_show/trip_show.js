const containerId = 'add_point_form_container'
const buttonId = 'add_point_with_url_button'
const hiddenClass = 'hidden'

function isInsideElement(target, container) {
    return element.closest(`#${container.id}`) != null
}

export function initAddPointButton() {
    let button = document.getElementById(buttonId)
    let container = document.getElementById(containerId)
    button.addEventListener('click', (ev) => {
        ev.preventDefault()
        container.classList.toggle(hiddenClass)
        // container.style.left = `${button.offsetLeft}px`
    })

    document.body.addClickListener(ev => {
        let { target } = ev
        if(!isInsideElement(target)) {
            container.classList.remove(hiddenClass)
        }
    })
}
