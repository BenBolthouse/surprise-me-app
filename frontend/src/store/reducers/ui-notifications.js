import { UINotificationCollection } from "../models/UINotification";

export const notificationManager = new UINotificationCollection();

const ADD_NOTIFICATION = "uiNotifications ———> ADD_NOTIFICATION";
const REMOVE_NOTIFICATION = "uiNotifications ———> REMOVE_NOTIFICATION";

/**
 * Adds a UI notification to the notifications collection and persists
 * entire collection to localStorage.
 *
 * @param {Object} config
 */
export const addUINotification = ({ body, type }) => ({
  type: ADD_NOTIFICATION,
  payload: { body, type, created_at: new Date().toISOString() },
});

/**
 * Removes a UI notification from the notifications collection and persists
 * entire collection to localStorage.
 *
 * @param {Object} config
 */
export const removeUINotification = ({ id }) => ({
  type: REMOVE_NOTIFICATION,
  payload: { id },
});

const reducer = (state = notificationManager.copy(), { type, payload }) => {
  switch (type) {
    case ADD_NOTIFICATION:
      notificationManager.add(payload);
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    case REMOVE_NOTIFICATION:
      notificationManager.remove(payload);
      notificationManager.syncToLocalStorage();
      return notificationManager.copy();

    default:
      return state;
  }
};

export default reducer;
