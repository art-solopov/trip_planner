import marker from './icons/marker.svg?raw'

export function makeMarker(pointElement) {
    const template = pointElement.querySelector('template[data-q=marker]')
    
    const el = document.importNode(template.content, true).firstElementChild
    el.insertAdjacentHTML('afterbegin', marker)
    return el
}
