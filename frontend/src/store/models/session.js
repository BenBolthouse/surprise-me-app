/** @module store/models/session */

import validate from "validate.js";
import { FatalError } from "../../services/ErrorHandler";
import { EntityBase } from "./Entity";

/**
 * @class
 * @abstract
 * @classdesc Represents a user session entity.
 */
export class Session extends EntityBase {
  /** @returns {this} */
  constructor(endpoint, csrfEndpoint) {
    super(endpoint);
    this.firstName = null;
    this.lastName = null;
    this.email = null;
    this.password = null;
    this.confirmPassword = null;
    this.bio = null;

    this.csrfEndpoint = csrfEndpoint;
    this.csrfToken = null;

    this.showValidationErrors = false;
    this.validationResult = true;
    this.validationErrors = {
      firstName: [],
      lastName: [],
      email: [],
      password: [],
      confirmPassword: [],
    };

    return this;
  }

  /**
   * Resets the validation property to its initial state and sets
   * showValidationErrors to false.
   * @returns {Session.validationErrors}
   */
  resetValidation() {
    this.showValidationErrors = false;
    
    this.validationErrors = {
      firstName: [],
      lastName: [],
      email: [],
      password: [],
      confirmPassword: [],
    };

    return this.validationErrors;
  }
  
  /**
   * Updates the session from the data object with mappable key value pairs
   * and runs validation on validation properties by default.
   * @param {object} data
   * @returns {this}
   */

  // prettier-ignore
  update({ firstName, lastName, email, password, confirmPassword, bio }) {
    this.firstName = firstName ? this._validate("firstName", firstName) : this.firstName;
    this.lastName = lastName ? this._validate("lastName", lastName) : this.lastName;
    this.email = email ? this._validate("email", email) : this.email;
    this.password = password ? this._validate("password", password) : this.password;
    this.confirmPassword = confirmPassword ? this._validateConfirmPassword(confirmPassword) : this.confirmPassword;
    this.bio = bio;

    return this;
  }

  /**
   * Throws an error if the session user does not exist.
   * @throws FatalError
   * @returns {this}
   */
  requireSession() {
    if (!this.id) throw new FatalError("You must be logged in to do this.")

    return this;
  }
  
  _validate(propertyName, value) {
    const schema = this._validationSchemas[propertyName];

    let result = validate(
      { [propertyName]: value },
      { [propertyName]: schema }
    );

    result = result ? result[propertyName] : [];

    this.validationErrors[propertyName] = result || [];

    this[propertyName] = value;

    if (result.length) this.validationResult = false;
    
    return value;
  }

  _validateConfirmPassword(value) {
    const schema = this._validationSchemas.confirmPassword;

    const result = validate(
      { confirmPassword: value, password: this.password },
      { confirmPassword: schema }
    );

    this.validationErrors.confirmPassword = result || [];

    this.confirmPassword = value;

    return value;
  }

  get _validationSchemas() {
    return {
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
    };
  }
}
