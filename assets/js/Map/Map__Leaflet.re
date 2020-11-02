module Ext = {
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
  [@bs.send]
  external mapContainer: _leaflet_map => Dom.element = "getContainer";
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
  external bindPopup: (_leaflet_marker, string) => _leaflet_marker =
    "bindPopup";
  [@bs.send]
  external addMarker: (_leaflet_marker, _leaflet_map) => unit = "addTo";
};

%bs.raw
{mljs|
  const MapIcon = L.Icon.extend({
      options: {
          iconSize: [34, 51],
          iconAnchor: [34 / 2, 51],
          popupAnchor: [0, -30]
      }
  })
|mljs};

[@bs.new]
external make__MapIcon: {. "iconUrl": string} => Ext._leaflet_icon =
  "MapIcon";

module Impl: Map__Builder.Lib = {
  type map = Ext._leaflet_map;
  let scriptSrc = "https://unpkg.com/leaflet@1.4.0/dist/leaflet.js";
  let container = Ext.mapContainer;
  let make = (el: Dom.element, options: Js.Dict.t(string)): map => {
    let dget = Js.Dict.unsafeGet;
    let map = Ext.(leaflet->map(el));
    let mapUrl = options->dget("mapUrl");
    let attribution = options->dget("attribution");

    let tiles =
      Ext.(leaflet->tileLayer(mapUrl, {"attribution": attribution}));
    tiles->Ext.addTileLayer(map);

    map;
  };
  let panTo = (map: map, coordinates: Map__Point.Coordinates.t) => {
    map->Ext.panTo(coordinates->Map__Point.Coordinates.toLatLon);
  };
  let fitBounds = (map, bounds: Map__Point.Coordinates.bounds) => {
    let convertedBounds =
      [|bounds.topLeft, bounds.botRight|]
      |> Array.map(Map__Point.Coordinates.toLatLon);
    let _ = map->Ext.fitBounds(convertedBounds);
    ();
  };
  let addMarker = (map, data: Map__Point.data) => {
    let icon = make__MapIcon({"iconUrl": data->Map__Point.iconUrl});
    let _ =
      Ext.(
        leaflet
        ->marker(
            data.coordinates->Map__Point.Coordinates.toLatLon,
            {"icon": icon},
          )
        ->bindPopup(data.name)
      )
      ->Ext.addMarker(map);
    ();
  };
};

module Builder = Map__Builder.Builder(Impl);
