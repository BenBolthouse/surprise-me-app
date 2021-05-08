import { addUINotification } from "../store/reducers/ui-notifications";
import { store } from "../index"

let created = false;

const DEBUG = true;
const DEFAULT_ERROR_MESSAGE = "There was a problem. Refreshing the page and try again."

/**
 * @class
 * @classdesc Service class provides a means of catching errors and
 * displaying error notifications to the user in a graceful manner.
 */
export default class ErrorHandler {
  /** @returns {this} */
  constructor() {
    if (created) throw new Error("Cannot create instance of singleton class");

    created = true;

    return this;
  }
  
  /**
   * Wrapper function for potentially hazardous operations.
   * @throws InfoError, WarningError or FatalError
   * @param {Function} callback Invokes callback in a try block to handle errors
   */
  async handler(callback) {
    if (DEBUG) return callback();
    
    // prettier-ignore
    try {
      await callback();
    }
    catch (error) {
      const body = error.message || DEFAULT_ERROR_MESSAGE;
      const type = error.type || "FATAL";
  
      switch (error.name) {
        case "InfoError":
          return store.dispatch(addUINotification({ body, type }));
          
        case "WarningError":
          return store.dispatch(addUINotification({ body, type }));
  
        case "FatalError":
          return store.dispatch(addUINotification({ body, type }));
  
        default:
          return store.dispatch(addUINotification({ body, type }));
      }
    }
  }
}

/**
 * @class
 * @classdesc Generate an error that carries an INFO type for creating UI
 * notifications.
 * @param {String} message Error message
 */
export class InfoError extends Error {
  constructor(message) {
    super(message);
    this.name = "InfoError";
    this.type = "INFO";
  }
}

/**
 * @class
 * @classdesc Generate an error that carries an WARNING type for creating
 * UI notifications.
 * @param {String} message Error message
 */
export class WarningError extends Error {
  constructor(message) {
    super(message);
    this.name = "WarningError";
    this.type = "WARNING";
  }
}

/**
 * @class
 * @classdesc Generate an error that carries an FATAL type for creating UI
 * notifications.
 * @param {String} message Error message
 */
export class FatalError extends Error {
  constructor(message) {
    super(message);
    this.name = "FatalError";
    this.type = "FATAL";
  }
}
