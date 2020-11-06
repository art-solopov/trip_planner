include DomBinds;

// Element is a wrapper for Dom._baseClass
type point = Map__Point.t(Dom._baseClass);

let getDataPoints = (): array(point) => {
  let elements = {
    let els = document->querySelectorAll("li.trip-point-item");
    Array.init(els->length, i => els->get(i));
  };

  elements |> Array.map(Map__Point.makeFromElement);
};

let panButtonClickHandler = (map: Map__Builder.unimap, dp: point) => {
  map.panTo(dp.data.coordinates);
  map.container
  ->scrollIntoView(Js.Dict.fromArray([|("behavior", "smooth")|]));
};

let main = () => {
  let mapEl =
    document->getElementById("map")->Js.Nullable.toOption->Belt.Option.getExn;
  let dataPoints = getDataPoints();
  let mapUrl = mapEl->dataset->Js.Dict.unsafeGet("mapUrl");
  let mapAttribution =
    document
    ->getElementById("map_attribution")
    ->Js.Nullable.toOption
    ->Belt.Option.mapWithDefault("", getInnerHTML);
  let bounds =
    Map__Point.Coordinates.boundsFromCoordinates(
      dataPoints |> Array.map((e: point) => e.data.coordinates),
    );
  bounds |> Js.log;

  let map =
    Map__Leaflet.Builder.build(
      mapEl,
      Js.Dict.fromArray([|
        ("mapUrl", mapUrl),
        ("attribution", mapAttribution),
      |]),
      Array.map((e: point) => e.data, dataPoints),
    );

  map.fitBounds(bounds);

  dataPoints
  |> Array.iter((dp: point) => {
       let _ =
         dp.el
         ->querySelector(".pan-link")
         ->Js.Nullable.toOption
         ->Belt.Option.map(f => {
             f->addClickListener(event => {
               event->preventDefault;
               panButtonClickHandler(map, dp);
             })
           });
       ();
     });
};
