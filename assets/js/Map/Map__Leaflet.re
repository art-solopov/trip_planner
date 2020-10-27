// TODO: extract all external data into another module (maybe External)

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

module Impl: Map__Builder.Lib = {
  type map = _leaflet_map;
  let scriptSrc = "https://unpkg.com/leaflet@1.4.0/dist/leaflet.js";

  [@bs.send] external _lmap: (_leaflet, Dom.element) => _leaflet_map = "map";
  [@bs.send] external _panTo: (map, array(float)) => unit = "panTo";
  [@bs.send]
  external _fitBounds: (map, array(array(float))) => _leaflet_map =
    "fitBounds";
  [@bs.send] external _addMarker: (_leaflet_marker, map) => unit = "addTo";

  [@bs.send] external container: map => Dom.element = "getContainer";
  let make = (el: Dom.element, options: Js.Dict.t(string)): map => {
    let dget = Js.Dict.unsafeGet;
    let map = leaflet->_lmap(el);
    let mapUrl = options->dget("mapUrl");
    let attribution = options->dget("attribution");

    let tiles = leaflet->tileLayer(mapUrl, {"attribution": attribution});
    tiles->addTileLayer(map);

    map;
  };
  let panTo = (map: map, coordinates: Map__Point.Coordinates.t) => {
    map->_panTo(coordinates->Map__Point.Coordinates.toLatLon);
  };
  let fitBounds = (map, bounds: Map__Point.Coordinates.bounds) => {
    let convertedBounds =
      [|bounds.topLeft, bounds.botRight|]
      |> Array.map(Map__Point.Coordinates.toLatLon);
    let _ = map->_fitBounds(convertedBounds);
    ();
  };
  let addMarker = (map, data: Map__Point.data) => {
    let icon = make__MapIcon({"iconUrl": data->Map__Point.iconUrl});
    let _ =
      leaflet
      ->marker(
          data.coordinates->Map__Point.Coordinates.toLatLon,
          {"icon": icon},
        )
      ->bindPopup(data.name)
      ->_addMarker(map);
    ();
  };
};

module Builder = Map__Builder.Builder(Impl);
