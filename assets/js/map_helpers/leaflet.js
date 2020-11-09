import L from 'leaflet'

const MapIcon = L.Icon.extend({
    options: {
        iconSize: [34, 51],
        iconAnchor: [34 / 2, 51],
        popupAnchor: [0, -30]
    }
})

// For reason
export function makeMapIcon(iconUrl) { return new MapIcon({iconUrl}); }

export { L }
