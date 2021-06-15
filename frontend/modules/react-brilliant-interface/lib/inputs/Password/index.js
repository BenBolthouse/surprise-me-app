/* eslint-disable react/prop-types */

import { createElement, useState } from "react";

import { InputErrors } from "../InputErrors";
import { InputEventHandler } from "../InputEventHandler";
import { ValidatedInput } from "../Input";

export function PasswordInput(props) {
  let { name, label, state, setState, validation, icons } = props;

  const [passwordVisible, setPasswordVisible] = useState(false);

  const inputComponent = {
    name,
    initialValue: "",
    state,
    setState,
    validation,
  };

  const inputEventHandlerComponent = {
    type: "password",
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
    type: passwordVisible ? "text" : "password",
    value: state.value,
    onChange: () => null, // Needed by React for bubbling, don't change.
  };

  const errorsComponent = {
    name,
    errors: state.errors,
  }

  const showPasswordElement =
    icons.showPassword && !passwordVisible
      ? createElement(
          "div",
          {
            className: "icon-show-password",
            onClick: function () {
              setPasswordVisible(true);
            },
          },
          icons.showPassword
        )
      : null;

  const hidePasswordElement =
    icons.hidePassword && passwordVisible
      ? createElement(
          "div",
          {
            className: "icon-hide-errors",
            onClick: function () {
              setPasswordVisible(false);
            },
          },
          icons.hidePassword
        )
      : null;

  return createElement(ValidatedInput, inputComponent,
    createElement(InputEventHandler, inputEventHandlerComponent,
      createElement("label", null, label),
      createElement("input", inputElement),
      createElement(InputErrors, errorsComponent),
      showPasswordElement,
      hidePasswordElement
    )
  );
}

