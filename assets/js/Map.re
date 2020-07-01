include DomBinds;

type point = Map__Point.t;

let leaflet = Map__Leaflet.leaflet;

let getDataPoints = (): array(point) => {
  let elements = {
    let els = document->querySelectorAll("li.trip-point-item");
    Array.init(els->length, i => els->get(i));
  };

  elements |> Array.map(Map__Point.makeFromElement);
};

let panButtonClickHandler = (map: Map__Leaflet._leaflet_map, dp: point) => {
  map->Map__Leaflet.panTo([|dp.data.lat, dp.data.lon|]);
  map
  ->Map__Leaflet.mapContainer
  ->scrollIntoView(Js.Dict.fromArray([|("behavior", "smooth")|]));
};

let main = () => {
  let mapEl = document->getElementById("map")->Belt.Option.getExn;
  let dataPoints = getDataPoints();
  let mapUrl = mapEl->dataset->Js.Dict.unsafeGet("mapUrl");
  let mapAttribution =
    document
    ->getElementById("map_attribution")
    ->Belt.Option.mapWithDefault("", getInnerHTML);
  let bounds = Map__Point.calculateBounds(dataPoints);
  bounds |> Js.log;
  let map =
    mapEl->Map__Leaflet.map(leaflet, _)->Map__Leaflet.fitBounds(bounds);
  let tileLayer =
    leaflet->Map__Leaflet.tileLayer(mapUrl, {"attribution": mapAttribution});
  tileLayer->Map__Leaflet.addTileLayer(map);

  Array.iter(
    (dp: point) => {
      Map__Leaflet.makeMarker(dp.data)->Map__Leaflet.addMarker(map);

      dp.el
      ->querySelector(".pan-link")
      ->Belt.Option.map(f =>
          f->addClickListener(event => {
            event->preventDefault;
            panButtonClickHandler(map, dp);
          })
        )
      ->Belt.Option.getWithDefault();
    },
    dataPoints,
  );
};