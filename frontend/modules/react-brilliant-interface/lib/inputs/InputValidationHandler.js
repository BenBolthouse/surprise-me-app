/* eslint-disable react/prop-types */

import { Fragment, useEffect, createElement } from "react";

import { validate } from "validate.js";

export function InputValidationHandler(props) {
  let { state, setState, validationAttributes, validationConstraints, children } = props;

  function validateAttributes() {
    const errors = validate(validationAttributes, validationConstraints);

    if (errors) setState({ ...state, errors: errors[0] });
    else setState({ ...state, errors: [] });
  }

  // Side effect validates input on every onchange event.
  useEffect(() => {
    validateAttributes();
  }, [state.value]);

  return createElement(Fragment, null, children);
}
