include DomBinds;

type data = {
  name: string,
  lat: float,
  lon: float,
  category: string // TODO replace with enum?
};

type t = {
  el: Dom.element,
  id: string,
  data,
};

let makeFromElement = (el: Dom.element): t => {
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
    {name, category, lat, lon};
  };
  {id: el->getId, data, el};
};

let calculateBounds = (pd: array(t)) => {
  let lats = pd |> Array.map(e => e.data.lat);
  let lons = pd |> Array.map(e => e.data.lon);

  let minLat = lats |> Array.fold_left(min, 100.0);
  let minLon = lons |> Array.fold_left(min, 100.0);
  let maxLat = lats |> Array.fold_left(max, -100.0);
  let maxLon = lons |> Array.fold_left(max, -100.0);

  [|[|minLat, minLon|], [|maxLat, maxLon|]|];
};
