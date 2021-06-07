/* eslint-disable react/prop-types */

import { createElement } from "react";

import { InputErrors, InputIconShowErrors, InputValidationHandler } from "../inputCommon";

function emailInput(props) {
  const { name, element, state, showErrorsIcon } = props;

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

  const showErrorsComponent = {
    key: name + "-input-icon-show-errors",
    name: name,
    errors: state.errors,
    icon: showErrorsIcon,
  }

  return createElement("div", null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
    createElement(InputIconShowErrors, showErrorsComponent),
  ])
}

export function EmailInput(props) {
  return createElement(InputValidationHandler, props,
    createElement(emailInput, props))
}

function passwordInput(props) {
  const { name, element, state, showErrorsIcon } = props;

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

  const showErrorsComponent = {
    key: name + "-input-icon-show-errors",
    name: name,
    errors: state.errors,
    icon: showErrorsIcon,
  }

  return createElement("div", null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
    createElement(InputIconShowErrors, showErrorsComponent),
  ])
}

export function PasswordInput(props) {
  return createElement(InputValidationHandler, props,
    createElement(passwordInput, props))
}
