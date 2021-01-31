include DomBinds

type container = Dom.element

let containerId = "add_point_form_container";
let hiddenClass = "hidden";

let hideContainer = (container) => {
  container->classList->ClassList.add(hiddenClass);
}

let showContainer = (container) => {
  container->classList->ClassList.remove(hiddenClass);
}

let isContainerHidden = (container) => {
  container->classList->ClassList.contains(hiddenClass);
}

let toggleContainer = (container) => {
  if(isContainerHidden(container)) {
    container->showContainer
  } else {
    container->hideContainer
  }
}

let isInsideElement = (element: Dom.element_like('a), testParent: Dom.element) => {
  element->closest("#" ++ testParent->getId)->Belt.Option.isSome
}

let initAddPointButton = () => {

  let button = document->getElementById("add_point_with_url_button")
    ->Belt.Option.getExn;
  let container = document->getElementById(containerId)
      ->Belt.Option.getExn;
  button->addClickListener(event => {
    event->preventDefault;
    container->toggleContainer;
    container->style->Style.setLeft(button->offsetLeft->Js.Int.toString ++ "px")
  })
  document->body->addClickListener(event => {
    let target = event->Event.target;
    if(!(target->isInsideElement(container) || target->isInsideElement(button))) {
      hideContainer(container)
    }
  })
}
