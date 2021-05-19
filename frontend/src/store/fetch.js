/* eslint-disable no-unused-vars */

import { store } from "..";

/** @module services/fetch */

import camelcase from "camelcase-keys";
import snakecase from "snakecase-keys";

import * as actions from "./actions";

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
  const csrf = store.getState().session.csrfToken;

  const defaultOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  };

  const request = { ...defaultOptions, ...options };

  const stateChangeReq = "POST PUT PATCH DELETE".includes(request.method);

  if (stateChangeReq) {
    if (request.body) {
      const convertCase = snakecase(request.body, { deep: true });
      request.body = JSON.stringify(convertCase);
    }
    request.headers["X-CSRFToken"] = csrf;
  }

  let response = await window.fetch(url, request);
  response = await response.json();
  response = camelcase(response, { deep: true });

  const { notification, data, status } = response;

  if (notification)
    switch (notification.type) {
      case "popup":
        store.dispatch(actions.notifications.popup.create(notification));
        break;
      case "card":
        store.dispatch(actions.notifications.card.create(notification));
        break;
    }

  if (status >= 400) throw Error();

  if (stateChangeReq) store.dispatch(actions.session.getCsrf());

  return data;
}
