/* eslint-disable react/prop-types */

import { createElement } from "react";

export function InputErrors(props) {
  let { name, errors } = props;

  if (errors.length) {
    const errorsElements = errors.map((error, i) => {
      const errorElement = {
        key: name + "-input-error-" + i,
        children: error,
      };
      return createElement("li", errorElement);
    });
    return createElement("ul", null, errorsElements);
  }

  return null;
}
