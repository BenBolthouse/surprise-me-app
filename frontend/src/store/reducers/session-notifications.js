/** @module store/reducers/session-notifications */

import { api, handler } from "../..";
import { SessionNotificationCollection } from "../models/Notification";
import { sessionManager } from "./session";

export const notificationManager = new SessionNotificationCollection();

const GET_NOTIFICATIONS = "sessionNotif... ———> GET_NOTIFICATIONS";
const SEE_NOTIFICATION = "sessionNotif... ———> SEE_NOTIFICATION";
const DISMISS_NOTIFICATION = "sessionNotif... ———> DISMISS_NOTIFICATION";

/**
 * Gets all of the non-dismissed notifications for the session user and
 * persists entire collection to localStorage.
 * @returns {true}
 */
export const getSessionNotifications = () => (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const action = (payload) => ({ type: GET_NOTIFICATIONS, payload });

  const { data } = await api.get(notificationManager.endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Adds datestamp for the moment a notification is seen and then
 * persists entire collection to localStorage.
 * @param {Array<Notification> | Notification} notifications
 * @returns {true}
 */
export const seeSessionNotification = (notifications) => (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const _n = notifications.length ? notifications : [notifications];

  const action = (payload) => ({ type: SEE_NOTIFICATION, payload });

  const endpoint = notificationManager.endpoint + "/see";

  const body = { notifications: _n}

  await api.patch(endpoint, body);

  dispatch(action(_n));

  return true;
});

/**
 * Adds datestamp for the moment a notification is seen and then
 * persists entire collection to localStorage.
 * @param {Array<Notification> | Notification} notifications
 * @returns {true}
 */
export const dismissSessionNotification = (notifications) => (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const _n = notifications.length ? notifications : [notifications];

  const action = (payload) => ({ type: DISMISS_NOTIFICATION, payload });

  const endpoint = notificationManager.endpoint + "/dismiss";

  const body = { notifications: _n}

  await api.patch(endpoint, body);

  dispatch(action(_n));

  return true;
});

const reducer = (state = notificationManager.copy(), { type, payload }) => {
  switch (type) {
    case GET_NOTIFICATIONS:
      notificationManager.produceFrom(payload);
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    case SEE_NOTIFICATION:
      payload.forEach((x) =>
        notificationManager.filter((y) => y.id == x.id).see()
      );
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    case DISMISS_NOTIFICATION:
      payload.forEach((x) =>
        notificationManager.filter((y) => y.id == x.id).dismiss()
      );
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    default:
      return state;
  }
};

export default reducer;
