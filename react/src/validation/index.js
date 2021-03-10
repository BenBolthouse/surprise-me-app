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
    pattern: /^(?:(?:[\w`~!#$%^&*\-=+;:{}\'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}\'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}\'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}\'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$/,
    message: "must be a valid email address.",
  },
};

export const passwordValidation = {
  password: {
    presence: {
      allowEmpty: false,
      message: "is required.",
    },
    format: {
      pattern: /^(?!.*\ )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$/,
      message:
        "must have at least one uppercase letter, lowercase letter, one special character and cannot contain spaces.",
    },
  },
  confirmPassword: {
    presence: {
      allowEmpty: false,
      message: "is required.",
    },
    equality: {
      attribute: "password",
      message: "must match password.",
    },
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
