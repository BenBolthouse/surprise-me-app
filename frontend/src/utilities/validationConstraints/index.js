export const required = {
  presence: {
    allowEmpty: false,
    message: "is required.",
  },
};

export const password = {
  format: {
    pattern:
      /^(?!.* )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$/,
    message:
      "must have at least one uppercase letter, lowercase letter, one special character and cannot contain spaces.",
  },
};

export const email = {
  format: {
    pattern:
      /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/,
    message: "must be a valid email address.",
  },
};
