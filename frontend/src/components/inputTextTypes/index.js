/* eslint-disable react/prop-types */

import { Fragment, createElement, useState } from "react";

import {
  InputErrors,
  InputIconOnErrors,
  InputStateHtmlHandler,
  InputValidationHandler,
} from "../inputCommon";

function emailInput(props) {
  const { name, element, state, setState, icons } = props;

  // Following is added to props dynamically via HTTP state wrapper in
  // inputCommon module:
  const { setTrying } = props;

  const inputElement = {
    key: name + "-input",
    type: "text",
    ...element,
    value: state.value,
    onChange: function (e) {
      setState({ ...state, value: e.target.value });
      setTrying(e.target.value.length > 0);
    },
  };

  const errorsComponent = {
    key: name + "-input-errors",
    name: name,
    errors: state.errors,
    element: {
      className: "errors",
    },
  };

  const showErrorsComponent = {
    key: name + "-input-icon-show-errors",
    errors: state.errors,
    icon: icons.showErrors,
    element: {
      className: "icon show-errors",
      onClick: function () {
        setState({ ...state, showErrors: true });
      },
    },
  };

  const hideErrorsComponent = {
    key: name + "-input-icon-hide-errors",
    errors: state.errors,
    icon: icons.hideErrors,
    element: {
      className: "icon hide-errors",
      onClick: function () {
        setState({ ...state, showErrors: false });
      },
    },
  };

  return createElement(Fragment, null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
    createElement(InputIconOnErrors, showErrorsComponent),
    createElement(InputIconOnErrors, hideErrorsComponent),
  ]);
}

export function EmailInput(props) {
  return createElement(
    InputValidationHandler,
    props,
    createElement(
      InputStateHtmlHandler,
      props,
      createElement(emailInput, props)
    )
  );
}

function passwordInput(props) {
  const { name, element, state, setState, icons } = props;

  // Following is added to props dynamically via HTTP state wrapper in
  // inputCommon module:
  const { setTrying } = props;

  const [showPassword, setShowPassword] = useState(false);

  const inputElement = {
    key: name + "-input",
    type: showPassword ? "text" : "password",
    ...element,
    value: state.value,
    onChange: function (e) {
      setState({ ...state, value: e.target.value });
      setTrying(e.target.value.length > 0);
    },
  };

  const errorsComponent = {
    key: name + "-input-errors",
    name: name,
    errors: state.errors,
    element: {
      className: "errors",
    },
  };

  const showErrorsComponent = {
    key: name + "-input-icon-show-errors",
    errors: state.errors,
    icon: icons.showErrors,
    element: {
      className: "icon show-errors",
      onClick: function () {
        setState({ ...state, showErrors: true });
      },
    },
  };

  const hideErrorsComponent = {
    key: name + "-input-icon-hide-errors",
    errors: state.errors,
    icon: icons.hideErrors,
    element: {
      className: "icon hide-errors",
      onClick: function () {
        setState({ ...state, showErrors: false });
      },
    },
  };

  function renderShowHidePasswordElementOrNull() {
    if (icons?.showPassword && icons?.hidePassword) {
      return createElement("div", {
        key: name + "-input-icon-show-hide-password",
        children: showPassword ? icons.hidePassword : icons.showPassword,
        className: "icon show-hide-password",
        onClick: function () {
          setShowPassword(!showPassword);
        },
      });
    }
    return null;
  }

  return createElement(Fragment, null, [
    createElement("input", inputElement),
    createElement(InputErrors, errorsComponent),
    createElement(InputIconOnErrors, showErrorsComponent),
    createElement(InputIconOnErrors, hideErrorsComponent),
    renderShowHidePasswordElementOrNull(),
  ]);
}

export function PasswordInput(props) {
  return createElement(
    InputValidationHandler,
    props,
    createElement(
      InputStateHtmlHandler,
      props,
      createElement(passwordInput, props)
    )
  );
}
