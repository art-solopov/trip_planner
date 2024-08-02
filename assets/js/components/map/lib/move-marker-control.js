import {iconsUrl} from '../../../utils'

export default class MoveMarkerControl {
    constructor(marker) {
        this._marker = marker
    }

    onAdd(map) {
        this._map = map;
        this._container = document.createElement('div');
        this._container.innerHTML = `
        <button title="Marker to center" data-action="map-pointer#setCoordinates" data-map-pointer-source-param="map">
            <i class="icon">target</i>
        </button>
        `
        this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';

        this._container.querySelector('button').addEventListener('click', () => this._marker.setLngLat(this._map.getCenter()))
        return this._container;
    }

    onRemove(map) {
        this._container.parentNode.removeChild(this._container);
        this._map = undefined;
    }
}
