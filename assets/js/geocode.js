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
        preview.src = e.map_url

        container.appendChild(el)
    }
}

function doGeocode(form, results, button, field) {
    button.disabled = true
    let search = form.querySelector(`[name=${field}]`).value
    let tripId = form.dataset.tripId

    axios.post('/api/geocode', { trip_id: tripId, search: search }).then(res => {
        displayGeocode(results, res.data);
        button.disabled = false
    })
}

function main() {
    let results = document.getElementById('geocode_results')
    let form = document.getElementById('point_form')

    for (let button of document.querySelectorAll('.btn-geocode')) {
        console.log(button)
        button.addEventListener('click', _ev => {
            doGeocode(form, results, button, button.dataset.field)
        })
    }


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
