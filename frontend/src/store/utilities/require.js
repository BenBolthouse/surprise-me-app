import { store } from "../../index";

let created = false;

export default class Require {
  constructor() {
    if (created) throw new Error("Cannot create instance of singleton class");

    created = true;
  }

  get state() {
    return store.getState()
  }

  /**
   * Determines if a session has been established by reading the Redux state
   * for a session id. Returns the session object or throws an error if not
   * found.
   */
  session() {
    const session = this.state.session;

    if (!session.id) {
      throw new Error("Session is required");
    }

    return session;
  }

  /**
   * Determines if a the csrf token is present. Returns true or throws an
   * error if not found.
   */
  csrf() {
    const token = this.state.session.csrfToken;

    if (!token) {
      throw new Error("Security token is missing");
    }

    return true;
  }
}
