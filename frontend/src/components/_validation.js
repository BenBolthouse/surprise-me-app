import { validate } from "validate.js";

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

export const password = (value) => {
  let result = validate({ password: value }, constraints.password);

  return result ? result.password : [];
};

export const confirmPassword = (value, confirmValue) => {
  let result = validate(
    { password: value, confirmPassword: confirmValue },
    constraints.confirmPassword
  );

  return result ? result.confirmPassword : [];
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
  password: {
    password: {
      presence: {
        allowEmpty: false,
        message: "is required.",
      },
      format: {
        pattern:
          /^(?!.* )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$/,
        message:
          "must have at least one uppercase letter, lowercase letter, one special character and cannot contain spaces.",
      },
    },
  },
  confirmPassword: {
    confirmPassword: {
      presence: {
        allowEmpty: false,
        message: "is required.",
      },
      equality: {
        attribute: "password",
        message: "must match password.",
        comparitor: (a, b) => a === b,
      },
    },
  },
};
