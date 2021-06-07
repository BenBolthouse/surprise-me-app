/* eslint-disable react/prop-types */

import { createElement } from "react";

import { InputErrors, InputValidationHandler } from "../inputCommon";

function emailInput(props) {
  const { name, element, state } = props;

  const inputElement = {
    key: name + "-input",
    type: "text",
    ...element,
  }

  const errorsComponent = {
    key: name + "-input-errors",
    name: name,
    errors: state.errors,
  }

  return createElement("div", null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
  ])
}

export function EmailInput(props) {
  return createElement(InputValidationHandler, props,
    createElement(emailInput, props))
}

function passwordInput(props) {
  const { name, element, state } = props;

  const inputElement = {
    key: name + "-input",
    type: "text",
    ...element,
  }

  const errorsComponent = {
    key: name + "-input-errors",
    name: name,
    errors: state.errors,
  }

  return createElement("div", null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
  ])
}

export function PasswordInput(props) {
  return createElement(InputValidationHandler, props,
    createElement(passwordInput, props))
}
