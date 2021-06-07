/* eslint-disable react/prop-types */

import { Fragment, useEffect, createElement } from "react";
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
