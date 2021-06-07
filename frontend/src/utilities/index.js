/** @module utilities */

import {
  destroy as _destroy,
  fetch as _fetch,
  get as _get,
  patch as _patch,
  post as _post,
} from "./fetch";

import * as _validationConstraints from "./validationConstraints";

/**
 * @async
 * @function
 * @description Convenience function invokes `utilities.fetch({..., method: "POST"})`.
 * @returns {object} Data and http status code as object `{ data, status }`
 */
export const post = _post;

/**
 * @async
 * @function
 * @description Convenience function invokes `utilities.fetch({..., method: "GET"})`.
 * @returns {object} Data and http status code as object `{ data, status }`
 */
export const get = _get;

/**
 * @async
 * @function
 * @description Convenience function invokes `utilities.fetch({..., method: "PATCH"})`.
 * @returns {object} Data and http status code as object `{ data, status }`
 */
export const patch = _patch;

/**
 * @async
 * @function
 * @description Convenience function invokes `utilities.fetch({..., method: "DELETE"})`.
 * @returns {object} Data and http status code as object `{ data, status }`
 */
export const destroy = _destroy;

/**
 * @async
 * @function
 * @description Ajax request utility using the browser's built in fetch API.
 * @returns {object} Data and http status code as object `{ data, status }`
 */
export const fetch = _fetch;

/**
 * @constant
 * @description Input constraints library utility for implementations of validate.js.
 */
export const validationConstraints = _validationConstraints;
