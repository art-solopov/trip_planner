module Ext = {
  type _leaflet;
  type _leaflet_map;
  type _leaflet_marker;
  type _leaflet_icon;
  type _leaflet_tile_layer;

  type point_data = Map__Point.data;

  type marker_config = {iconUrl: string};

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

  let import = (): Js.Promise.t(_leaflet) => {
    %raw
    "import('leaflet')";
  };
};

// TODO: make it async somehow?
%bs.raw
{mljs|
  import('leaflet').then(L => {
    const MapIcon = L.Icon.extend({
        options: {
            iconSize: [34, 51],
            iconAnchor: [34 / 2, 51],
            popupAnchor: [0, -30]
        }
    })

    window.MapIcon = MapIcon
  })
|mljs};

[@bs.new]
external make__MapIcon: {. "iconUrl": string} => Ext._leaflet_icon =
  "MapIcon";

module Impl: Map__Builder.Lib = {
  type map = Ext._leaflet_map;
  let container = Ext.mapContainer;

  let import = Ext.import();

  let make = (el: Dom.element, options: Js.Dict.t(string)) => {
    let dget = Js.Dict.unsafeGet;
    let mapUrl = options->dget("mapUrl");
    let attribution = options->dget("attribution");

    import
    |> Js.Promise.(
         then_(leaflet => {
           let map = Ext.(leaflet->map(el));
           let tiles =
             Ext.(leaflet->tileLayer(mapUrl, {"attribution": attribution}));
           tiles->Ext.addTileLayer(map);

           resolve(map);
         })
       );
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
      import
      |> Js.Promise.then_(leaflet => {
           leaflet
           ->Ext.marker(
               data.coordinates->Map__Point.Coordinates.toLatLon,
               {"icon": icon},
             )
           ->Ext.bindPopup(data.name)
           ->Ext.addMarker(map);
           Js.Promise.resolve();
         });
    ();
  };
};

module Builder = Map__Builder.Builder(Impl);
