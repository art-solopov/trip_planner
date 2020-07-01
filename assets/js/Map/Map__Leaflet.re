type _leaflet;
type _leaflet_map;
type _leaflet_marker;
type _leaflet_icon;
type _leaflet_tile_layer;

type point_data = Map__Point.data;

type marker_config = {iconUrl: string};

[@bs.val] external leaflet: _leaflet = "L";
[@bs.send] external map: (_leaflet, Dom.element) => _leaflet_map = "map";
[@bs.send] external panTo: (_leaflet_map, array(float)) => unit = "panTo";
[@bs.send] external mapContainer: _leaflet_map => Dom.element = "getContainer";
[@bs.send]
external fitBounds: (_leaflet_map, array(array(float))) => _leaflet_map =
  "fitBounds";
[@bs.send]
external tileLayer:
  (_leaflet, string, {. "attribution": string}) => _leaflet_tile_layer =
  "tileLayer";
[@bs.send]
external addTileLayer: (_leaflet_tile_layer, _leaflet_map) => unit = "addTo";
[@bs.send]
external marker:
  (_leaflet, array(float), {. "icon": _leaflet_icon}) => _leaflet_marker =
  "marker";
[@bs.send]
external bindPopup: (_leaflet_marker, string) => _leaflet_marker = "bindPopup";
[@bs.send]
external addMarker: (_leaflet_marker, _leaflet_map) => unit = "addTo";

%bs.raw
{mljs| const MapIcon = L.Icon.extend({
                options: {
                    iconSize: [34, 51],
                    iconAnchor: [34 / 2, 51],
                    popupAnchor: [0, -30]
                }
            }) |mljs};

[@bs.new]
external make__MapIcon: {. "iconUrl": string} => _leaflet_icon = "MapIcon";

let makeMarker = (pd: point_data) => {
  let icon =
    make__MapIcon({"iconUrl": "/static/icons/" ++ pd.category ++ ".png"});
  leaflet->marker([|pd.lat, pd.lon|], {"icon": icon})->bindPopup(pd.name);
};