import { EntityBase } from "./base";

export class Session extends EntityBase {
  constructor(endpoint, csrfEndpoint) {
    super(endpoint);
    this._csrfEndpoint = csrfEndpoint;
    this._csrfToken = null;
    this._firstName = null;
    this._lastName = null;
    this._email = null;
    this._bio = null;
  }

  get csrfEndpoint() {
    return this._csrfEndpoint;
  }
  get csrfToken() {
    return this._csrfToken;
  }
  get firstName() {
    return this._firstName;
  }
  get lastName() {
    return this._lastName;
  }
  get email() {
    return this._email;
  }
  
  setCsrfToken({ token }) {
    this._csrfToken = token;
  }

  /**
   * Method required by base class for populating data from api responses.
   *
   * @param {object} responseData 
   */
  populate({ first_name, last_name, email, bio }) {
    this._firstName = first_name;
    this._lastName = last_name;
    this._email = email;
    this._bio = bio;
  }
}
