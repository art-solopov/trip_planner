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

function doGeocode(button, form, results) {
    button.disabled = true
    let tripId = form.dataset.tripId
    let name = form.querySelector('input[name=name]').value
    let address = form.querySelector('textarea[name=address]').value
    let field = form.querySelector('input[name=geocode_field]:checked')
    if(field) {
        field = field.value
    }

    let data = {
        trip_id: tripId,
        name: name,
        address: address,
        field: field
    }

    axios.post('/api/geocode', data, { headers: { 'X-Device-Dims': `${window.screen.width}x${window.screen.height}` } }).then(res => {
        displayGeocode(results, res.data);
        button.disabled = false
    })
}

export default function main() {
    let results = document.getElementById('geocode_results')
    let form = document.getElementById('point_form')
    let button = document.getElementById('btn_geocode')

    button.addEventListener('click', ev => {
        doGeocode(button, form, results)
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


