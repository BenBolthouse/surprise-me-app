import { validate } from "validate.js"

export const firstName = (value) => {
  let result = validate({ firstName: value }, constraints.firstName);

  return result ? result.firstName : [];
};

export const lastName = (value) => {
  let result = validate({ lastName: value }, constraints.lastName);

  return result ? result.lastName : [];
};

export const email = (value) => {
  let result = validate({ email: value }, constraints.email);

  return result ? result.email : [];
};

const constraints = {
  firstName: {
    firstName: {
      presence: {
        allowEmpty: false,
        message: "is required.",
      },
      format: {
        pattern: /^([A-Za-z'-]+)$/,
        message: "cannot have any numbers, special characters or spaces.",
      },
    },
  },
  lastName: {
    lastName: {
      presence: {
        allowEmpty: false,
        message: "is required.",
      },
      format: {
        pattern: /^([A-Za-z'-]+)$/,
        message: "cannot have any numbers, special characters or spaces.",
      },
    },
  },
  email: {
    email: {
      presence: {
        allowEmpty: false,
        message: "is required.",
      },
      format: {
        pattern:
          /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/,
        message: "must be a valid email address.",
      },
    },
  },
};
