include DomBinds;

type datum = {
  lat: float,
  lon: float,
  address: string,
  name: string,
  map_url: string,
};

let displayGeocode = (container: Dom.element, data: array(datum)) => {
  container->setInnerHTML("");

  if (Array.length(data) == 0) {
    container->setInnerHTML(
      "<span class=\"text-error\">No geocode results found</span>",
    );
  } else {
    let template =
      document
      ->getElementById("geocode_result_template")
      ->Js.Nullable.toOption
      ->Belt.Option.getExn;

    data
    |> Array.iter(e => {
         let el =
           document
           ->importNode(template->getContent, true)
           ->querySelector("div")
           ->Js.Nullable.toOption
           ->Belt.Option.getExn;
         let dataset = el->dataset;
         dataset->Js.Dict.set("lat", e.lat->Js.Float.toString);
         dataset->Js.Dict.set("lon", e.lon->Js.Float.toString);

         el
         ->querySelector(".address")
         ->Js.Nullable.toOption
         ->Belt.Option.getExn
         ->setTextContent(e.address);
         el
         ->querySelector(".name")
         ->Js.Nullable.toOption
         ->Belt.Option.getExn
         ->setTextContent(e.name);

         el
         ->querySelectorImage(".preview")
         ->Js.Nullable.toOption
         ->Belt.Option.getExn
         ->setSrc(e.map_url);
         ();

         container->appendChild(el);
       });
  };
};

type input_shape =
  | Input
  | Textarea;

let formValue =
    (form: Dom.htmlFormElement, ~inputShape: input_shape=Input, field: string) => {
  let selector =
    switch (inputShape) {
    | Input => "input"
    | Textarea => "textarea"
    };

  form
  ->querySelectorInput({j|$(selector)[name=$(field)]|j})
  ->Js.Nullable.toOption
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
      let address = form->formValue(~inputShape=Textarea, "address");
      let field =
        form
        ->querySelectorInput("input[name=geocode_field]:checked")
        ->Js.Nullable.toOption
        ->Belt.Option.map(getValue);

      let data = {
        "trip_id": tripId->int_of_string,
        "name": name,
        "address": address,
        "field": field,
      };

      let _promise =
        Js.Promise.(
          Axios.postData("/api/geocode", data)
          |> then_(response => {resolve(response##data)})
          |> then_(data => {
               displayGeocode(results, data);
               button->setDisabled(false);
               resolve(data);
             })
        );
      ();
    }
  );

let resultsListener = (form: Dom.htmlFormElement, event: Dom.event_like('a)) => {
  let target = event->Event.target;

  if (target->classList->ClassList.contains("gc-save")) {
    let parent =
      target
      ->closest(".geocode-result")
      ->Js.Nullable.toOption
      ->Belt.Option.getExn;

    form
    ->querySelectorInput("input[name=lat]")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn
    ->setValue(parent->dataset->Js.Dict.unsafeGet("lat"));

    form
    ->querySelectorInput("input[name=lon]")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn
    ->setValue(parent->dataset->Js.Dict.unsafeGet("lon"));

    target
    ->closest("#geocode_results")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn
    ->setInnerHTML("");
  };
};

let default = () => {
  let results =
    document
    ->getElementById("geocode_results")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;
  let form =
    document
    ->getElementByIdForm("point_form")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;
  let button =
    document
    ->getElementByIdInput("btn_geocode")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;

  button->addClickListener(_event => {
    doGeocode(button, form, results);
    ();
  });

  results->addClickListener(resultsListener(form));
};
