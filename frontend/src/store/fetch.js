import { store } from "../index";

const defaults = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
};

/**
 * Base fetch API customized for connection to the service API.
 *
 * @param {String} url URL for the request
 * @param {object} options Config object for fetch API function
 */
export const fetch = async (url, options = {}) => {
  const request = { ...defaults, ...options };

  // Following attempts to find the csrf token in the Redux state with
  // every state-changing API request (POST, PATCH, PUT, DELETE). If the
  // csrf token returns null then the function throws an error.
  const csrfToken = store.getState().session._csrfToken;

  if (request.method.toUpperCase() !== "GET") {
    // Throw an exception if the Redux state does not have a valid csrf
    // token.
    if (!csrfToken) {
      throw Error("Invalid or missing security token.");
    }
    request.body = JSON.stringify(options.body);
    request.headers["X-CSRFToken"] = csrfToken;
  }

  const response = await window.fetch(url, request);
  const body = await response.json();
  const { message, data } = body;

  if (response.status >= 400) throw response;

  return { message, data };
};
