/* eslint-disable react/prop-types */

import { Fragment, useEffect, createElement as element } from "react";
import { validate } from "validate.js";

export function InputErrors({ name, errors }) {
  if (errors && errors.length) {
    const errorsElements = () =>
      errors.map((error, i) => {
        const errorElement = {
          key: name + "-input-error-" + i,
          children: error,
        };
        return element("li", errorElement);
      });
    return element("ul", null, errorsElements());
  } else {
    return null;
  }
}

export function InputIconShowErrors({ errors, icon}) {
  if (errors && errors.length) {
    const iconElement = {
      className: "input-icon-show-errors",
      children: icon,
    }
    return element("div", iconElement);
  } else {
    return null;
  }
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
    const errors = validate(
      validationAttributes,
      validationConstraints,
    );
    if (errors) {
      setState({ ...state, errors: errors[name] });
    } else {
      setState({ ...state, errors: [] });
    }
  }

  useEffect(() => {
    validateAttributes();
  }, [state.value]);

  return element(Fragment, null, children)
}
