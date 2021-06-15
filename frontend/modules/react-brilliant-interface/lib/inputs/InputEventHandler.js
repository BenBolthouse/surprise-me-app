/* eslint-disable react/prop-types */

import { createElement, useEffect, useState } from "react";

export function InputEventHandler(props) {
  let { name, type, state, setState, validation, options, children, icons } = props;

  // Default options if none are provided.
  options = options || {};
  options.trackTrying = options.trackTrying || true;
  options.trackTried = options.trackTried || true;
  options.trackFocused = options.trackFocused || true;
  options.tryOn = options.tryOn || "onchange";

  // Default icons if none are provided.
  icons = icons || {};

  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);
  const [focused, setFocused] = useState(false);
  const [hasErrors, setHasErrors] = useState(false);
  const [errorsVisible, setErrorsVisible] = useState(false);

  // Side effect sets state of has errors in relation to the length of the
  // error array.
  useEffect(() => {
    setHasErrors(!state.errors ? hasErrors : state.errors.length > 0);
  }, [state.errors])

  const eventHandlerElementClasses = [
    `${name} input-group input-group-${type} `,
    options.trackTrying ? (trying ? "trying " : "not-trying ") : "",
    options.trackTried ? (tried ? "tried " : "not-tried ") : "",
    options.trackFocus ? (focused ? "focused " : "not-focused ") : "",
    validation ? (hasErrors ? "errors " : "no-errors ") : "",
    validation ? (errorsVisible ? "errors-visible " : "errors-hidden ") : "",
  ];

  const eventHandlerElement = {
    className: eventHandlerElementClasses.join("").trim(),
    onLoad: function() {
      options.tryOn === "onload" && setTried(true);
    },
    onChange: function(e) {
      setState({...state, value: e.target.value});
      options.tryOn === "onchange" && setTried(true);

      if (e.target.value) setTrying(true);
      else setTrying(false);
    },
    onFocus: function() {
      setFocused(true);
      options.tryOn === "onfocus" && setTried(true);
    },
    onBlur: function() {
      setFocused(false);
      options.tryOn === "onblur" && setTried(true);
    },
  }

  const showErrorsElement =
    !errorsVisible && icons.showErrors && state.errors && state.errors.length
      ? createElement(
          "div",
          {
            className: "icon-show-errors",
            onClick: function () {
              setErrorsVisible(true);
            },
          },
          icons.showErrors
        )
      : null;

  const hideErrorsElement =
    errorsVisible && icons.showErrors && state.errors && state.errors.length
      ? createElement(
          "div",
          {
            className: "icon-hide-errors",
            onClick: function () {
              setErrorsVisible(false);
            },
          },
          icons.hideErrors
        )
      : null;

  return createElement("div", eventHandlerElement,
    children,
    showErrorsElement,
    hideErrorsElement
  );
}
