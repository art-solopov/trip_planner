function displayGeocode(container, data) {
    container.innerHTML = ""

    if (data.length == 0) {
        container.innerHTML = '<span class="text-error">No geocode results found</span>'
        return
    }

    const template = document.getElementById('geocode_result_template')

    for (let e of data) {
        let el = document.importNode(template.content, true).querySelector('div')
        el.dataset.lat = e.lat
        el.dataset.lon = e.lon

        el.querySelector('.address').innerText = e.address
        el.querySelector('.name').innerText = e.name

        let preview = el.querySelector('.preview')
        let previewSrc = preview.src
        previewSrc = previewSrc.replace(/\$lat/g, e.lat).replace(/\$lon/g, e.lon)
        preview.src = previewSrc

        container.appendChild(el)
    }
}

function main() {
    let button = document.getElementById('btn_geocode')
    let results = document.getElementById('geocode_results')
    let form = button.closest('form')

    let link = button.dataset.link
    let tripId = button.dataset.tripId

    button.addEventListener('click', (ev) => {
        button.disabled = true
        let address = form.querySelector('textarea[name=address]').value
        let name = form.querySelector('input[name=name]').value

        axios.post(link, { trip_id: tripId, search: address || name }).then(res => {
            displayGeocode(results, res.data);
            button.disabled = false
        })
    })

    results.addEventListener('click', (ev) => {
        let {target} = ev
        if (!target.classList.contains('gc-save')) return;

        let parent = target.closest('.geocode-result')
        form.querySelector('input[name=lat]').value = parent.dataset.lat
        form.querySelector('input[name=lon]').value = parent.dataset.lon

        target.closest('#geocode_results').innerHTML = ''
    })
}

main()
