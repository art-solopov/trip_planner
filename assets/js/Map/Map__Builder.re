type markerConfig = {iconUrl: string};

module Coordinates = Map__Point.Coordinates;
type coordinates = Coordinates.t;
type bounds = Coordinates.bounds;
type data = Map__Point.data;

module type Lib = {
  type map;
  let scriptSrc: string;

  let make: (Dom.element, Js.Dict.t(string)) => Js.Promise.t(map);
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
  type mapPromise = Js.Promise.t(t);

  let mapChange = (mapPromise, func: t => unit): unit => {
    let _ =
      Js.Promise.(
        mapPromise
        |> then_(map => {
             func(map);
             resolve(map);
           })
      );
    ();
  };

  let mapWrapper = (mapPromise, func: (t, 'a) => unit) => {
    let wrapped = (mapPromise, arg: 'a) => {
      mapPromise->mapChange(map => func(map, arg));
    };
    wrapped(mapPromise);
  };

  let build =
      (element: Dom.element, options: Js.Dict.t(string), data: array(data)) => {
    let mapPromise = MapImpl.make(element, options);

    mapPromise->mapChange(map => Array.iter(map->MapImpl.addMarker, data));
    let obj: unimap = {
      container: element,
      panTo: mapPromise->mapWrapper(MapImpl.panTo),
      fitBounds: mapPromise->mapWrapper(MapImpl.fitBounds),
    };
    obj;
  };
};
