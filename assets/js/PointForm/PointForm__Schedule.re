module Row = {
  type t = {
    el: Dom.element,
    openFrom: Dom.htmlInputElement,
    openTo: Dom.htmlInputElement,
  };

  type data = {
    openFrom: string,
    openTo: string,
  };

  let make = (rowel: Dom.element) => {
    {
      el: rowel,
      openFrom:
        rowel
        ->DomBinds.querySelectorInput("input[name$=open_from]")
        ->Js.Nullable.toOption
        ->Belt.Option.getExn,
      openTo:
        rowel
        ->DomBinds.querySelectorInput("input[name$=open_to]")
        ->Js.Nullable.toOption
        ->Belt.Option.getExn,
    };
  };

  let fromInput = (input: Dom.htmlInputElement) =>
    make(
      input->DomBinds.closest("tr")->Js.Nullable.toOption->Belt.Option.getExn,
    );

  let data = (row: t) =>
    DomBinds.{openFrom: row.openFrom->getValue, openTo: row.openTo->getValue};

  let setData = (row: t, d: data) => {
    open DomBinds;
    row.openFrom->setValue(d.openFrom);
    row.openTo->setValue(d.openTo);
  };
};

let default = () => {
  open DomBinds;

  let currentInput: ref(option(Dom.htmlInputElement)) = ref(None);

  let scheduleButtons =
    document
    ->getElementById("schedule_buttons")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;

  Js.log(scheduleButtons);

  let copyDownButton =
    scheduleButtons
    ->querySelector(".btn-copy-down")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;

  let copyAllButton =
    scheduleButtons
    ->querySelector(".btn-copy-all")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;

  scheduleButtons->classList->ClassList.remove("hidden");

  let scheduleTable =
    document
    ->getElementById("schedule")
    ->Js.Nullable.toOption
    ->Belt.Option.getExn;

  scheduleTable->addFocusinListener(event => {
    let target = event->Event.target;
    currentInput := Some(target);
    scheduleButtons
    ->style
    ->Style.setTop(target->offsetParent->offsetTop->Js.Int.toString ++ "px");
  });

  copyDownButton->addClickListener(_event => {
    let row = Row.fromInput((currentInput^)->Belt.Option.getExn);
    let _ =
      row.el
      ->nextElementSibling
      ->Js.Nullable.toOption
      ->Belt.Option.map(nextRowEl => {
          let nextRow = Row.make(nextRowEl);
          Row.(nextRow->setData(row->data));
          nextRow.openFrom->focus();
          ();
        });
    ();
  });

  copyAllButton->addClickListener(_event => {
    let row = Row.fromInput((currentInput^)->Belt.Option.getExn);
    let rowdata = row->Row.data;

    let rowEls = scheduleTable->querySelectorAll("tbody tr");
    Belt.Range.forEach(
      0,
      rowEls->length - 1,
      i => {
        let urow = Row.make(rowEls->get(i));
        urow->Row.setData(rowdata);
        ();
      },
    );
    ();
  });
};
