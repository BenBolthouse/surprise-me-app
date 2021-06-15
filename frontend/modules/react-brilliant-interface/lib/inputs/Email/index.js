/* eslint-disable react/prop-types */

import { createElement } from "react";

import { InputErrors } from "../InputErrors";
import { InputEventHandler } from "../InputEventHandler";
import { ValidatedInput } from "../Input";

export function EmailInput(props) {
  let { name, label, state, setState, validation, icons } = props;

  const inputComponent = {
    name,
    initialValue: "",
    state,
    setState,
    validation,
  };

  const inputEventHandlerComponent = {
    type: "email",
    name,
    state,
    setState,
    validation,
    options: {
      trackTrying: true,
      trackTried: true,
      trackFocused: true,
    },
    icons,
  }

  const inputElement = {
    type: "text",
    value: state.value,
    onChange: () => null, // Needed by React for bubbling, don't change.
  };

  const errorsComponent = {
    name,
    errors: state.errors,
  }

  return createElement(ValidatedInput, inputComponent,
    createElement(InputEventHandler, inputEventHandlerComponent,
      createElement("label", null, label),
      createElement("input", inputElement),
      createElement(InputErrors, errorsComponent)
    )
  );
}
