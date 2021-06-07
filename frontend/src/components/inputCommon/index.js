/* eslint-disable react/prop-types */

import {
  Fragment,
  useEffect,
  createElement,
  useState,
  cloneElement,
} from "react";
import { validate } from "validate.js";

export function InputErrors(props) {
  let { name, errors, element } = props;

  if (!element) element = {};

  // prettier-ignore
  if (errors && errors.length) {
    const errorsElements = () =>
      errors.map((error, i) => {
        const errorElement = {
          key: name + "-input-error-" + i,
          children: error,
        };
        return createElement("li", errorElement);
      });
    return createElement("ul", element, errorsElements());
  }
  else return null;
}

export function InputIconOnErrors(props) {
  let { errors, icon, element } = props;

  if (!element) element = {};

  // prettier-ignore
  if (errors && errors.length) {
    return createElement("div", element, icon);
  }
  else return null;
}

export function InputValidationHandler(props) {
  const {
    name,
    state,
    setState,
    validationAttributes,
    validationConstraints,
    children,
  } = props;

  function validateAttributes() {
    const errors = validate(validationAttributes, validationConstraints);
    if (errors) {
      setState({ ...state, errors: errors[name] });
    } else {
      setState({ ...state, errors: [] });
    }
  }

  useEffect(() => {
    validateAttributes();
  }, [state.value]);

  return createElement(Fragment, null, children);
}

export function InputStateHtmlHandler(props) {
  let { state, tryOn, children: input } = props;

  if (!tryOn) tryOn = "onchange";

  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);
  const [focused, setFocused] = useState(false);
  const [showErrors, setShowErrors] = useState(false);

  const wrapperElement = {
    "br-trying": trying.toString(),
    "br-tried": tried.toString(),
    "br-focused": focused.toString(),
    "br-show-errors": showErrors.toString(),
    onLoad: function () {
      if (tryOn === "onload") setTried(true);
    },
    onChange: function () {
      if (tryOn === "onchange") setTried(true);
    },
    onFocus: function () {
      if (tryOn === "onfocus") setTried(true);
    },
    onBlur: function () {
      if (tryOn === "onblur") setTried(true);
    },
  };

  // Side effect detects changes of showErrors in state and updates this
  // component's state, accordingly.
  useEffect(() => {
    setShowErrors(state.showErrors);
  }, [state.showErrors]);

  const childInputClone = cloneElement(input, {
    ...input.props,
    setTrying,
    setTried,
    setFocused,
    setShowErrors,
  });

  return createElement("div", wrapperElement, childInputClone);
}
