import {iconsUrl} from '../../../utils'
import styles from './marker-styles.module.css'
import icons from './icons'

export function pointMarkerElement(category) {
    return markerElement(
        `is-${category}`,
        [markerBase(), markerCategoryIcon(category)].join("\n")
    )
}

export function draggableMarkerElement() {
    return markerElement(styles.draggableMarker, markerBase())
}

function markerElement(addClass, innerHTML) {
    const el = document.createElement('div')
    el.className = styles.marker
    if(addClass) el.classList.add(addClass)
    el.innerHTML = innerHTML
    return el
}

function markerBase() {
    return `<svg class=${styles.markerBody}><use xlink:href="${iconsUrl}#marker" /></svg>`
}

function markerCategoryIcon(category) {
    return `<img class=${styles.markerIcon} src=${icons[category]}></img>`
}
