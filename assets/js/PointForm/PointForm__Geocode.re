include DomBinds;

type datum = {
  lat: float,
  lon: float,
  address: string,
  name: string,
  map_url: string,
};

let displayGeocode = (container: Dom.element, data: array(datum)) =>
  if (Array.length(data) == 0) {
    container->setInnerHTML(
      "<span class=\"text-error\">No geocode results found</span>",
    );
  } else {
    let template =
      document->getElementById("geocode_result_template")->Belt.Option.getExn;

    data
    |> Array.iter(e => {
         let el = document->importNode(template->getContent, true);
         let dataset = el->dataset;
         dataset->Js.Dict.set("lat", e.lat->Js.Float.toString);
         dataset->Js.Dict.set("lon", e.lon->Js.Float.toString);

         el
         ->querySelector(".address")
         ->Belt.Option.getExn
         ->setTextContent(e.address);
         el
         ->querySelector(".name")
         ->Belt.Option.getExn
         ->setTextContent(e.name);

         el
         ->querySelectorImage(".preview")
         ->Belt.Option.getExn
         ->setSrc(e.map_url);
         ();

         container->appendChild(el);
       });
  };

let formValue = (form: Dom.htmlFormElement, field: string) => {
  form
  ->querySelectorInput({j|input[name=$(field)]|j})
  ->Belt.Option.getExn
  ->getValue;
};

let doGeocode =
  Dom.(
    (button: htmlInputElement, form: htmlFormElement, results: element) => {
      button->setDisabled(true);
      let formDs = form->dataset;
      let tripId = formDs->Js.Dict.unsafeGet("tripId");
      let name = form->formValue("name");
      let address = form->formValue("address");
      let field =
        form
        ->querySelectorInput("input[name=geocode_field]:checked")
        ->Belt.Option.map(getValue);

      let data = {
        "trip_id": tripId->int_of_string,
        "name": name,
        "address": address,
        "field": field,
      };

      Js.Promise.(
        Axios.postData("/api/geocode", data)
        |> then_(response => {resolve(response##data)})
        |> then_(data => {
             displayGeocode(results, data);
             button->setDisabled(false);
             resolve(data);
           })
      );
    }
  );
