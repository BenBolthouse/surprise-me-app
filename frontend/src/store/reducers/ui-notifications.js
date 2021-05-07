import { UINotificationCollection } from "../models/UINotification"

const notificationManager = new UINotificationCollection();

const ADD_NOTIFICATION = "uiNotifications ———> ADD_NOTIFICATION";
const REMOVE_NOTIFICATION = "uiNotifications ———> REMOVE_NOTIFICATION";

export const addUINotification = ({ body, type }) => ({
  type: ADD_NOTIFICATION,
  payload: { body, type, created_at: new Date().toISOString() },
});

export const removeUINotification = ({ id }) => ({ type: REMOVE_NOTIFICATION, payload: { id } })

const reducer = (state = notificationManager.state(), { type, payload }) => {
  switch (type) {
    case ADD_NOTIFICATION:
      notificationManager.add(payload)
      notificationManager.syncToLocalStorage()
      return notificationManager.state();

    case REMOVE_NOTIFICATION:
      notificationManager.remove(payload)
      notificationManager.syncToLocalStorage()
      return notificationManager.state();

    default:
      return state;
  }
};

export default reducer;
