module ClassList = {
  type t;
  [@bs.send] external contains: (t, string) => bool = "contains";
  [@bs.send] external remove: (t, string) => unit = "remove";
};

module Event = {
  type i('a) = Dom.event_like('a);

  [@bs.get] external target: i('a) => Dom.element_like('b) = "target";
};

module Style = {
  type t;

  [@bs.get] external getTop: t => string = "top";
  [@bs.set] external setTop: (t, string) => unit = "top";
};

type classList = ClassList.t;

type _htmlImageElement;
type htmlImageElement = Dom.htmlElement_like(_htmlImageElement);
[@bs.set] external setSrc: (htmlImageElement, string) => unit = "src";

[@bs.set]
external setDisabled: (Dom.htmlInputElement, bool) => unit = "disabled";
[@bs.get] external getValue: Dom.htmlInputElement => string = "value";
[@bs.set] external setValue: (Dom.htmlInputElement, string) => unit = "value";

[@bs.val] external document: Dom.document = "document";
[@bs.send]
external querySelectorAll: (Dom.node_like('a), string) => Dom.nodeList =
  "querySelectorAll";
[@bs.send]
external getElementById: (Dom.document, string) => Js.Nullable.t(Dom.element) =
  "getElementById";
[@bs.send]
external getElementByIdInput:
  (Dom.document, string) => Js.Nullable.t(Dom.htmlInputElement) =
  "getElementById";
[@bs.send]
external getElementByIdForm:
  (Dom.document, string) => Js.Nullable.t(Dom.htmlFormElement) =
  "getElementById";
[@bs.get_index] external get: (Dom.nodeList, int) => Dom.element;
[@bs.get] external length: Dom.nodeList => int = "length";
[@bs.get]
external dataset: Dom.element_like('a) => Js.Dict.t(string) = "dataset";
[@bs.get] external classList: Dom.element_like('a) => classList = "classList";
[@bs.get] external style: Dom.element_like('a) => Style.t = "style";
[@bs.get]
external offsetParent: Dom.element_like('a) => Dom.element = "offsetParent";
[@bs.get] external offsetTop: Dom.element_like('a) => int = "offsetTop";
[@bs.get]
external nextElementSibling:
  Dom.element_like('a) => Js.Nullable.t(Dom.element) =
  "nextElementSibling";
[@bs.send]
external querySelector:
  (Dom.node_like('a), string) => Js.Nullable.t(Dom.element) =
  "querySelector";
[@bs.send]
external querySelectorImage:
  (Dom.node_like('a), string) => Js.Nullable.t(htmlImageElement) =
  "querySelector";
[@bs.send]
external querySelectorInput:
  (Dom.node_like('a), string) => Js.Nullable.t(Dom.htmlInputElement) =
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
external addFocusinListener:
  (Dom.eventTarget_like('a), [@bs.as "focusin"] _, Dom.event => unit) => unit =
  "addEventListener";
[@bs.send]
external scrollIntoView: (Dom.element, Js.Dict.t(string)) => unit =
  "scrollIntoView";
[@bs.send]
external appendChild: (Dom.element_like('a), Dom.node_like('b)) => unit =
  "appendChild";
[@bs.send]
external closest:
  (Dom.element_like('a), string) => Js.Nullable.t(Dom.element_like('b)) =
  "closest";
[@bs.send]
external focus:
  (
    Dom.element_like('a),
    ~options: {. "preventScroll": option(bool)}=?,
    unit
  ) =>
  unit =
  "focus";
[@bs.send] external preventDefault: Dom.event => unit = "preventDefault";
