import { EntityBase } from "./Entity";

export class Session extends EntityBase {
  constructor(endpoint, csrfEndpoint) {
    super(endpoint);
    this.csrfEndpoint = csrfEndpoint;
    this.csrfToken = null;
    this.firstName = null;
    this.lastName = null;
    this.email = null;
    this.bio = null;
  }

  /**
   * Method required by base class.
   *
   * @param {object} responseObject
   * @return {null} `null`
   */
  populate({ first_name, last_name, email, bio }) {
    this.firstName = first_name;
    this.lastName = last_name;
    this.email = email;
    this.bio = bio;
  }
}
