// State template
const notificationsTemplate = {
  timestamp: null,
  chat: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const SYNC_REDUX_LOCAL_NOTIFICATIONS = "notifications/syncReduxLocalOnLoad";
/**
 * Populate Redux notification state from local storage
 * state on app renders. If the target
 * `localStorage.notifications` object is `null` then this
 * function sets the local storage object for subsequent
 * renders.
 */
export const syncReduxLocalOnLoad = () => ({
  type: SYNC_REDUX_LOCAL_NOTIFICATIONS,
});

const SET_CHAT_NOTIFICATION = "notifications/setChatNotification";
/**
 * Add a new chat notification message to both Redux and
 * local storage states with an id as key.
 *
 * @param {*} object Contains required arguments integer
 * `id` and string `message`. E.g. for id `333` and message
 * `"Hello World"`, the resulting message will be stored in
 * both stores as: `«storeKey»: [ 333: "Hello World" ]`
 */
export const setChatNotification = ({ id, message }) => ({
  type: SET_CHAT_NOTIFICATION,
  payload: { id, message },
});

const DELETE_CHAT_NOTIFICATION = "notifications/deleteChatNotification";
/**
 * Delete a chat notification from both Redux and local
 * storage states by id.
 *
 * @param {*} object Contains required argument integer
 * `id`, where `id` is the the ID of the message for
 * deletion.
 */
export const deleteChatNotification = (id) => ({
  type: DELETE_CHAT_NOTIFICATION,
  payload: id,
});

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = notificationsTemplate, { type, payload }) => {
  
  // Scoped variables
  let locStateObj;
  let reduxStateObj;

  switch (type) {

    case SYNC_REDUX_LOCAL_NOTIFICATIONS:
      locStateObj = JSON.parse(
        localStorage.getItem("notifications")
      );
      if (locStateObj === null) {
        localStorage.setItem("notifications", JSON.stringify({ chat: {} }));
        return {
          ...state,
        };
      }
      return {
        ...state,
        timestamp: new Date().toISOString(),
        chat: locStateObj.chat,
      };

    case SET_CHAT_NOTIFICATION:
      locStateObj = JSON.parse(
        localStorage.getItem("notifications")
      );
      locStateObj.chat = {
        ...locStateObj.chat,
        [payload.id]: payload.message,
      };
      localStorage.setItem(
        "notifications",
        JSON.stringify(locStateObj)
      );
      return {
        ...state,
        chat: {
          ...state.chat,
          [payload.id]: payload.message,
        },
      };

    case DELETE_CHAT_NOTIFICATION:
      locStateObj = JSON.parse(
        localStorage.getItem("notifications")
      );
      delete locStateObj.chat[payload];
      localStorage.setItem(
        "notifications",
        JSON.stringify(locStateObj)
      );
      reduxStateObj = { ...state.chat };
      delete reduxStateObj[payload];
      return { ...state, chat: reduxStateObj };

    default:
      return state;
  }
};

export default reducer;
