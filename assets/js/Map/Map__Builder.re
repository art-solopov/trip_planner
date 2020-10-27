type markerConfig = {iconUrl: string};

module Coordinates = Map__Point.Coordinates;
type coordinates = Coordinates.t;
type bounds = Coordinates.bounds;
type data = Map__Point.data;

module type Lib = {
  type map;
  let scriptSrc: string;

  let make: (Dom.element, Js.Dict.t(string)) => map;
  let container: map => Dom.element;
  let panTo: (map, coordinates) => unit;
  let fitBounds: (map, bounds) => unit;
  let addMarker: (map, data) => unit;
};

type unimap = {
  container: Dom.element,
  panTo: coordinates => unit,
  fitBounds: bounds => unit,
};

module Builder = (MapImpl: Lib) => {
  type t = MapImpl.map;
  type data = Map__Point.data;

  let build =
      (element: Dom.element, options: Js.Dict.t(string), data: array(data)) => {
    let map = MapImpl.make(element, options);
    // _trueMap := Some(map);
    Array.iter(map->MapImpl.addMarker, data);

    let obj: unimap = {
      container: element,
      panTo: map->MapImpl.panTo,
      fitBounds: map->MapImpl.fitBounds,
    };
    obj;
  };
};
