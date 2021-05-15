/** @module services/fetch */

import { store } from ".";
import camelcase from "camelcase-keys";
import snakecase from "snakecase-keys";
import userManager from "./store/models/user.model";
import * as notificationActions from "./store/reducers/notification.reducer";

/**
 * Sends a get request.
 * @param {String} url Request URL
 * @returns {Promise<{message: String, data: object | Array}>}
 * @throws WarningError on 400 range errors and FatalError on 500 range errors
 */
export async function get(url) {
  return await this.fetch(url, { method: "GET" });
}

/**
 * Sends a post request.
 * @param {String} url Request URL
 * @param {object | Array} body Request data
 * @returns {Promise<{message: String, data: object | Array}>}
 * @throws WarningError on 400 range errors and FatalError on 500 range errors
 */
export async function post(url, body) {
  return await this.fetch(url, { method: "POST", body });
}

/**
 * Sends a put request.
 * @param {String} url Request URL
 * @param {object | Array} body Request data
 * @returns {Promise<{message: String, data: object | Array}>}
 * @throws WarningError on 400 range errors and FatalError on 500 range errors
 */
export async function put(url, body) {
  return await this.fetch(url, { method: "PUT", body });
}

/**
 * Sends a patch request.
 * @param {String} url Request URL
 * @param {object | Array} body Request data
 * @returns {Promise<{message: String, data: object | Array}>}
 * @throws WarningError on 400 range errors and FatalError on 500 range errors
 */
export async function patch(url, body) {
  return await this.fetch(url, { method: "PATCH", body });
}

const defaultOptions = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
};

/**
 * Sends a delete request.
 * @param {String} url Request URL
 * @returns {Promise<{message: String, data: object | Array}>}
 * @throws WarningError on 400 range errors and FatalError on 500 range errors
 */
export async function destroy(url) {
  return await this.fetch(url, { method: "DELETE" });
}

/** @ignore */
export async function fetch(url, options = {}) {
  const request = { ...defaultOptions, ...options };

  if ("POST PUT PATCH DELETE".includes(request.method)) {
    if (request.body) {
      const convertCase = snakecase(request.body, { deep: true });
      request.body = JSON.stringify(convertCase);
    }
    request.headers["X-CSRFToken"] = userManager.csrfToken;
  }

  let response = await window.fetch(url, request);
  response = await response.json();
  response = camelcase(response, { deep: true });

  const { notification, data, status } = response;

  if (notification) {
    store.dispatch(notificationActions.addNotification(notification));
  }

  if (status >= 400) throw Error();

  return { data };
}
