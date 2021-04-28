import validate from "validate.js";

export const nameValidation = {
  presence: {
    allowEmpty: false,
    message: "is required.",
  },
  format: {
    pattern: /^([A-Za-z'-]+)$/,
    message: "cannot have any numbers, special characters or spaces.",
  },
};

export const emailValidation = {
  presence: {
    allowEmpty: false,
    message: "is required.",
  },
  format: {
    pattern: /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/,
    message: "must be a valid email address.",
  },
};

export const passwordValidation = {
  presence: {
    allowEmpty: false,
    message: "is required.",
  },
  format: {
    pattern: /^(?!.* )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$/,
    message:
      "must have at least one uppercase letter, lowercase letter, one special character and cannot contain spaces.",
  },
};

export const requiredValidation = {
  presence: {
    allowEmpty: false,
    message: "is required.",
  },
};

export const checkboxValidation = {
  inclusion: {
    within: [true],
    message: "must be selected.",
  },
};

/**
 * Validates a state object and loads validation results
 * into an "errors" property on the state object.
 *
 * E.g. if state object `email` is provided then property
 * `email.value` is validated. If validation fails then
 * property `email.errors` is populated with validation
 * results. Callback argument `setStateObject`, the set
 * function of `useState`, is invoked to update state.
 *
 * The function assumes the following initial state variable
 * structure, using the example above:
 * ```
 * email: {
 *   name: "email",
 *   value: "",
 *   errors: [],
 *   ...
 * }
 * ```
 *
 * If the above data structure isn't used then the
 * validation will write the `value` and `errors` properties
 * into the object using spread. It's recommended to use
 * this structure for happy and carefree validation.
 *
 * @param {*} stateObject `useState` variable
 * @param {*} setStateObject Corresponding `useState` set function for `stateObject`
 * @param {*} constraints Validator.js constraints object
 * @param {*} event Optional: DOM event to update state
 * object value prior to validation.
 * @returns {*} `true` or `false` if validation succeeds or fails, respectively.
 */
export const stateValidation = async (
  stateObject,
  setStateObject,
  constraints,
  event
) => {
  // If event present then use the event target value
  const value = event ? event.target.value : stateObject.value;
  // Run validation
  const result = validate({ [stateObject.name]: value }, constraints);
  // If validation fails...
  if (result) {
    // Get all errors to a single array
    let errors = [];
    errors = Object.keys(result).map((key) => [...errors, ...result[key]]);
    // Update state
    setStateObject({ ...stateObject, errors });

    return false;
  }
  // If validation succeeds then clear errors
  setStateObject({ ...stateObject, errors: [], errorsVisible: false });
  return true;
};
