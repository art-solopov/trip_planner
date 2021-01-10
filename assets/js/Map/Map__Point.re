include DomBinds;

module Coordinates = {
  type t = {
    lat: float,
    lon: float,
  };

  type bounds = {
    topLeft: t,
    botRight: t,
  };

  let make = (lat, lon): t => {lat, lon};
  let makeBounds = (topLeft: t, botRight: t) => {topLeft, botRight};
  let boundsFromCoordinates = (coordinates: array(t)) => {
    let lats = Array.map(e => e.lat, coordinates);
    let lons = Array.map(e => e.lon, coordinates);
    {
      topLeft: {
        lat: lats |> Array.fold_left(min, 100.0),
        lon: lons |> Array.fold_left(min, 100.0),
      },
      botRight: {
        lat: lats |> Array.fold_left(max, -100.0),
        lon: lons |> Array.fold_left(max, -100.0),
      },
    };
  };
  let toLatLon = (c: t) => [|c.lat, c.lon|];
};

type data = {
  name: string,
  coordinates: Coordinates.t,
  category: string // TODO replace with enum?
};

type el('a) = Dom.element_like('a);

type t('a) = {
  el: el('a),
  id: string,
  data,
};

let makeFromElement = (el: el('a)): t('a) => {
  let data: data = {
    let ds = el->dataset;
    let name =
      el
      ->querySelector(".item-name")
      ->Belt.Option.map(getInnerText)
      ->Belt.Option.getExn;
    let category = ds->Js.Dict.unsafeGet("category");
    let lat = ds->Js.Dict.unsafeGet("lat")->Js.Float.fromString;
    let lon = ds->Js.Dict.unsafeGet("lon")->Js.Float.fromString;
    {
      name,
      category,
      coordinates: {
        lat,
        lon,
      },
    };
  };
  {id: el->getId, data, el};
};

let iconUrl = (item: data) => {
  "/static/icons/" ++ item.category ++ ".png";
};
