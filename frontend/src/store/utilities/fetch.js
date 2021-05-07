import { store } from "../../index";
import { FatalError, WarningError } from "./error-handler";

// prettier-ignore
const defaults = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
};

/**
 * REST fetch a resource from the API, or change backend state. The world
 * is your oyster. Formats responses in a predictable way, which is
 * fundamental for excellent backend/frontend state synchrony.
 *
 * Returns a message/data object in the format of `{message: string, data?:
 * object}`. Data should be an object literal, also super important for
 * Redux.
 *
 * @param {String} url URL for the request
 * @param {object} options Config object for the OG fetch API
 * @return {Promise<{message: String, data: object}>}
 */
export const fetch = async (url, options = {}) => {
  const request = { ...defaults, ...options };

  // Following attempts to find the csrf token in the Redux state with
  // every state-changing API request (POST, PATCH, PUT, DELETE). If the
  // csrf token returns null then the function throws an error.
  const csrfToken = store.getState().session.csrfToken;

  if (request.method.toUpperCase() !== "GET") {
    // Throw an exception if the Redux state does not have a valid csrf
    // token.
    if (!csrfToken) throw new WarningError();

    request.body = JSON.stringify(options.body);

    request.headers["X-CSRFToken"] = csrfToken;
  }

  const response = await window.fetch(url, request);

  const body = await response.json();

  const { message, data } = body;

  if (response.status >= 400 && response.status < 500) {
    throw new WarningError(message);
  }

  if (response.status >= 500) {
    throw new FatalError(message);
  }

  return { message, data };
};
