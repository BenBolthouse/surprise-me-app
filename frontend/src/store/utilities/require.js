import { store } from "../../index";
import { FatalError, WarningError } from "./error-handler";

let created = false;

/**
 * Singleton service class provides checkpoints for required state
 * components in order to proceed compiling code. Invoke methods ahead of
 * compiling Redux actions and thunks. Require methods can be thought of as
 * "decorators" for Redux.
 */
export default class Require {
  /**
   * Invoke constructor in store index module as singleton service.
   */
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
      throw new WarningError("You must be logged in to do this. Please log in and try again.");
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
      throw new FatalError();
    }

    return true;
  }
}
