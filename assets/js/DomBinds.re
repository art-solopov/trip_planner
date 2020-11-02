type _htmlImageElement;
type htmlImageElement = Dom.htmlElement_like(_htmlImageElement);
[@bs.set] external setSrc: (htmlImageElement, string) => unit = "src";

[@bs.set]
external setDisabled: (Dom.htmlInputElement, bool) => unit = "disabled";
[@bs.get] external getValue: Dom.htmlInputElement => string = "value";

[@bs.val] external document: Dom.document = "document";
[@bs.send]
external querySelectorAll: (Dom.node_like('a), string) => Dom.nodeList =
  "querySelectorAll";
[@bs.send]
external getElementById: (Dom.document, string) => option(Dom.element) =
  "getElementById";
[@bs.get_index] external get: (Dom.nodeList, int) => Dom.element;
[@bs.get] external length: Dom.nodeList => int = "length";
[@bs.get]
external dataset: Dom.element_like('a) => Js.Dict.t(string) = "dataset";
[@bs.send]
external querySelector: (Dom.node_like('a), string) => option(Dom.element) =
  "querySelector";
[@bs.send]
external querySelectorImage:
  (Dom.node_like('a), string) => option(htmlImageElement) =
  "querySelector";
[@bs.send]
external querySelectorInput:
  (Dom.node_like('a), string) => option(Dom.htmlInputElement) =
  "querySelector";
[@bs.get] external getInnerText: Dom.element => string = "innerText";
[@bs.get] external getInnerHTML: Dom.element_like('a) => string = "innerHTML";
[@bs.set]
external setInnerHTML: (Dom.element_like('a), string) => unit = "innerHTML";
[@bs.set]
external setTextContent: (Dom.element_like('a), string) => unit =
  "textContent";
[@bs.get] external getContent: Dom.element => string = "content";
[@bs.get] external getId: Dom.element_like('a) => string = "id";
[@bs.send]
external importNode: (Dom.document, string, bool) => Dom.node_like('a) =
  "importNode";
[@bs.send]
external addClickListener:
  (Dom.eventTarget_like('a), [@bs.as "click"] _, Dom.event => unit) => unit =
  "addEventListener";
[@bs.send]
external scrollIntoView: (Dom.element, Js.Dict.t(string)) => unit =
  "scrollIntoView";
[@bs.send]
external appendChild: (Dom.element, Dom.node_like('a)) => unit =
  "appendChild";
[@bs.send] external preventDefault: Dom.event => unit = "preventDefault";
