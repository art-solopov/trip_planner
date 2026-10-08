export function elementOnScreen(element) {
    let rect = element.getBoundingClientRect()
    return rect.top >= 0 && rect.top <= window.innerHeight && rect.bottom >= 0
}

export const iconsUrl = document.querySelector('meta[name="js:icons_url"]').content

// Taken from https://www.freecodecamp.org/news/javascript-debounce-example/
export function debounce(func, timeout = 300) {
    let timer
    return (...args) => {
        clearTimeout(timer)
        timer = setTimeout(() => { func.apply(this, args) }, timeout)
    }
}
