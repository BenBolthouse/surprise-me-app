import { FatalError, WarningError } from "./ErrorHandler";
import camelcase from "camelcase-keys";
import snakecase from "snakecase-keys";

let created = false;

/**
 * @class
 * @classdesc Service class provides a more robust fetch API that formats
 * requests and responses in a predictable manner.
 * @param {String} csrfToken Anti-forgery token
 */
export default class Fetch {
  /** @returns {this} */
  constructor(csrfToken) {
    if (created) throw new Error("Cannot create instance of singleton class");

    created = true;

    this.csrfToken = csrfToken || "";

    this.defaultOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    }

    return this;
  }

  /** 
   * Sends a get request.
   * @param {String} url Request URL
   * @returns {Promise<{message: String, data: object | Array}>}
   * @throws WarningError on 400 range errors and FatalError on 500 range errors
   */
  async get(url) {
    return await this.fetch(url, { method: "GET" });
  }

  /**
   * Sends a post request.
   * @param {String} url Request URL
   * @param {object | Array} body Request data
   * @returns {Promise<{message: String, data: object | Array}>}
   * @throws WarningError on 400 range errors and FatalError on 500 range errors
   */
  async post(url, body) {
    return await this.fetch(url, { method: "POST", body });
  }

  /**
   * Sends a put request.
   * @param {String} url Request URL
   * @param {object | Array} body Request data
   * @returns {Promise<{message: String, data: object | Array}>}
   * @throws WarningError on 400 range errors and FatalError on 500 range errors
   */
  async put(url, body) {
    return await this.fetch(url, { method: "PUT", body });
  }

  /**
   * Sends a patch request.
   * @param {String} url Request URL
   * @param {object | Array} body Request data
   * @returns {Promise<{message: String, data: object | Array}>}
   * @throws WarningError on 400 range errors and FatalError on 500 range errors
   */
  async patch(url, body) {
    return await this.fetch(url, { method: "PATCH", body });
  }

  /**
   * Sends a delete request.
   * @param {String} url Request URL
   * @returns {Promise<{message: String, data: object | Array}>}
   * @throws WarningError on 400 range errors and FatalError on 500 range errors
   */
  async delete(url) {
    return await this.fetch(url, { method: "DELETE" });
  }

  /**
   * Sets the CSRF token.
   * @returns {true}
   */
  setCsrfToken(token) {
    this.csrfToken = token;

    return true;
  }

  /** @ignore */
  async fetch(url, options = {}) {
    const request = { ...this.defaultOptions, ...options };

    if ("POST PUT PATCH DELETE".includes(request.method)) {
      if (request.body) {
        request.body = snakecase(request.body, { deep: true });
        request.body = JSON.stringify(options.body);
      }
      request.headers["X-CSRFToken"] = this.csrfToken;
    }

    let response = await window.fetch(url, request);
    response = await response.json();
    response = camelcase(response, { deep: true });

    const {message, data} = response;

    if (response.status >= 400 && response.status < 500) {
      throw new WarningError(message);
    }
  
    if (response.status >= 500) {
      throw new FatalError(message);
    }
  
    return { message, data };
  }
}
