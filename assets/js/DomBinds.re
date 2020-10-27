[@bs.val] external document: Dom.document = "document";
[@bs.send]
external querySelectorAll: (Dom.node_like('a), string) => Dom.nodeList =
  "querySelectorAll";
[@bs.send]
external getElementById: (Dom.document, string) => option(Dom.element) =
  "getElementById";
[@bs.get_index] external get: (Dom.nodeList, int) => Dom.element;
[@bs.get] external length: Dom.nodeList => int = "length";
[@bs.get] external dataset: Dom.element => Js.Dict.t(string) = "dataset";
[@bs.send]
external querySelector: (Dom.node_like('a), string) => option(Dom.element) =
  "querySelector";
[@bs.get] external getInnerText: Dom.element => string = "innerText";
[@bs.get] external getInnerHTML: Dom.element => string = "innerHTML";
[@bs.get] external getId: Dom.element => string = "id";
[@bs.send]
external addClickListener:
  (Dom.eventTarget_like('a), [@bs.as "click"] _, Dom.event => unit) => unit =
  "addEventListener";
[@bs.send]
external scrollIntoView: (Dom.element, Js.Dict.t(string)) => unit =
  "scrollIntoView";
[@bs.send] external preventDefault: Dom.event => unit = "preventDefault";