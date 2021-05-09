/** @module store/reducers/ui-notifications */

import { UINotificationCollection } from "../models/Notification";

export const notificationManager = new UINotificationCollection();

const ADD_NOTIFICATION = "uiNotifications ———> ADD_NOTIFICATION";
const SEE_NOTIFICATION = "uiNotifications ———> SEE_NOTIFICATION";
const DISMISS_NOTIFICATION = "uiNotifications ———> DISMISS_NOTIFICATION";

/**
 * Adds a UI notification to the notifications collection and persists
 * entire collection to localStorage.
 * @param {String} body
 * @returns Redux action for reducer
 */
export const addUINotification = (body) => {
  const createdAt = new Date().toISOString();

  const type = "INFO";

  return { type: ADD_NOTIFICATION, payload: { body, type, createdAt } };
};

/**
 * Adds datestamp for the moment a notification is seen and then persists
 * entire collection to localStorage.
 * @param {String} id
 * @returns Redux action for reducer
 */
export const seeUINotification = (id) => {
  notificationManager.filter((x) => x.id === id).see();

  return { type: SEE_NOTIFICATION, payload: { id } };
};

/**
 * Adds datestamp for the moment a notification is dismissed and then
 * persists entire collection to localStorage.
 * @param {String} id
 * @returns Redux action for reducer
 */
export const dismissUINotification = (id) => {
  notificationManager.filter((x) => x.id === id).dismiss();

  return { type: DISMISS_NOTIFICATION, payload: { id } };
};

const reducer = (state = notificationManager.copy(), { type, payload }) => {
  switch (type) {
    case ADD_NOTIFICATION:
      notificationManager.produceFrom([payload]);
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    case SEE_NOTIFICATION:
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    case DISMISS_NOTIFICATION:
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    default:
      return state;
  }
};

export default reducer;
