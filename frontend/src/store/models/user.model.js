import { EntityBase } from "../entity";

class User extends EntityBase {
  constructor() {
    super(
      {
        firstName: "String",
        lastName: "String",
        email: "String",
        localImagePath: "String",
        bio: "String",
        latitude: "Float",
        longitude: "Float",
        password: "String",
        confirmPassword: "String",
      },
      {
        validation: true,
        validationProps: _validationProps,
        validationSchema: _validationSchema,
      }
    );

    this.csrfToken = null;
    this.registrationSteps ={
      nameAndEmailComplete: false,
      pictureAndBioComplete: false,
      geolocationComplete: false,
      passwordComplete: false,
    }

  }

  completeNameAndEmail(complete) {
    this.registrationSteps.nameAndEmailComplete = complete || false;

    return this;
  }

  completePictureAndBio(complete) {
    this.registrationSteps.pictureAndBioComplete = complete || false;

    return this;
  }

  completeGeolocation(complete) {
    this.registrationSteps.geolocationComplete = complete || false;

    return this;
  }

  completePassword(complete) {
    this.registrationSteps.passwordComplete = complete || false;

    return this;
  }
}

const _validationProps = [
  "firstName",
  "lastName",
  "email",
  "password",
  "confirmPassword",
  "latitude",
  "longitude",
];

const _validationSchema = {
  firstName: {
    presence: {
      allowEmpty: false,
      message: "First name is required.",
    },
    format: {
      pattern: /^([A-Za-z'-]+)$/,
      message:
        "First name cannot have any numbers, special characters or spaces.",
    },
  },

  lastName: {
    presence: {
      allowEmpty: false,
      message: "Last name is required.",
    },
    format: {
      pattern: /^([A-Za-z'-]+)$/,
      message:
        "Last name cannot have any numbers, special characters or spaces.",
    },
  },

  email: {
    presence: {
      allowEmpty: false,
      message: "An email is required.",
    },
    format: {
      pattern: /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/,
      message: "Email must be a valid email address.",
    },
  },

  password: {
    presence: {
      allowEmpty: false,
      message: "A password is required.",
    },
    format: {
      pattern: /^(?!.* )(?=.*\d)(?=.+\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,32}$/,
      message:
        "Password must have at least one uppercase letter, lowercase letter, one special character, one number and cannot contain spaces.",
    },
  },

  confirmPassword: {
    equality: {
      attribute: "password",
      message: "Confirm password doesn't match password.",
      comparitor: (a, b) => a === b,
    },
  },

  latitude: {
    presence: {
      allowEmpty: false,
      message: "Latitude coordinate value required."
    }
  },

  longitude: {
    presence: {
      allowEmpty: false,
      message: "Latitude coordinate value required."
    }
  },
};

const userManager = new User();

export default userManager;
