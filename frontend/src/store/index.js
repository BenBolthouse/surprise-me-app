/** @module store */

import {socketIoClient as _socketIoClient} from "./socketIoClient";
import * as _actions from "./actions";

/**
 * @constant
 * @description Redux actions library
 */
export const actions = _actions;

/**
 * @constant
 * @description SocketIO configuration and events routes.
 */
export const socketIoClient = _socketIoClient;
