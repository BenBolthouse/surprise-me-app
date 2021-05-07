import { addUINotification } from "../reducers/ui-notifications";
import { store } from "../../index"

const DEFAULT_ERROR_MESSAGE = "There was a problem. Refreshing the page and try again."

/**
 * Generate an error that carries an INFO type for creating UI notifications.
 * 
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
 * Generate an error that carries an WARNING type for creating UI notifications.
 * 
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
 * Generate an error that carries an FATAL type for creating UI notifications.
 * 
 * @param {String} message Error message
 */
export class FatalError extends Error {
  constructor(message) {
    super(message);
    this.name = "FatalError";
    this.type = "FATAL";
  }
}

/**
 * Wrapper function for any potentially dangerous operations. Rather than
 * exposing ugly errors to the user, the result is a pleasant and
 * log-friendly UI notification.
 *
 * Any errors tripped here will generate a notification that can be viewed
 * either in Redux state or the client's localStorage as item
 * `notifications_ui`.
 *
 * @param {Function} callback Invokes callback in a try block to handle errors
 */
export default async function handler(callback) {
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
