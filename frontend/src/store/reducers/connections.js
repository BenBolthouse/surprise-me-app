import { fetch } from "../../services/fetch";
import { normalize } from "../../services/normalize";

// State template
const stateTemplate = {
  timestamp: null,
  established: {},
  pending: {},
  awaiting: {},
  notifications: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const GET_CONNECTIONS = "connections/getConnections";
export const getConnections = () => async (dispatch) => {
  const res = await fetch("/api/connections");
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: GET_CONNECTIONS,
      payload,
    }))(data)
  );
  return res;
};

const SPOOF_MESSAGE_CONNECTION = "chat/spoofMsgConnection";
export const spoofMessageConnection = (connId) => ({
  type: SPOOF_MESSAGE_CONNECTION,
  payload: connId,
});

const GET_CHAT_NOTIFICATIONS = "chat/getChatNotifications";
export const getChatNotifications = () => async (dispatch) => {
  const url = "/api/chat_notifications";
  const res = await fetch(url);
  let { data } = res.data;
  data = normalize(data, "userConnectionId");
  dispatch(
    ((payload) => ({
      type: GET_CHAT_NOTIFICATIONS,
      payload,
    }))(data)
  );
  return res;
};

const UPDATE_CHAT_NOTIFICATION = "chat/updateChatNotification";
export const updateChatNotification = (notification) => ({
  type: UPDATE_CHAT_NOTIFICATION,
  payload: notification,
});

const CLEAR_CHAT_NOTIFICATION = "chat/clearChatNotification";
export const clearChatNotification = (connId) => async (dispatch) => {
  const url = `/api/chat_notifications/${connId}`;
  const res = await fetch(url, {
    method: "DELETE",
  });
  dispatch(
    ((payload) => ({
      type: CLEAR_CHAT_NOTIFICATION,
      payload,
    }))(connId)
  );
  return res;
};

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = stateTemplate, { type, payload }) => {
  switch (type) {
    // ********************
    case GET_CONNECTIONS:
      const estConnections = payload.filter((c) => {
        if (c.establishedAt !== null) return c;
        return false;
      });
      const pendingConnections = payload.filter((c) => {
        if (c.establishedAt === null) return c;
        return false;
      });
      return {
        ...state,
        timestamp: new Date().toISOString(),
        established: normalize(estConnections),
        pending: normalize(pendingConnections),
      };
    // ********************
    case SPOOF_MESSAGE_CONNECTION:
      return {
        ...state,
        established: {
          ...state.established,
          [payload]: {
            ...state.established[payload],
            lastMessage: {
              body: "",
              createdAt: new Date().toUTCString(),
              sender: {
                id: null,
              },
            },
          },
        },
      };
    // ********************
    case GET_CHAT_NOTIFICATIONS:
      return {
        ...state,
        notifications: payload,
      };
    // ********************
    case UPDATE_CHAT_NOTIFICATION:
      return {
        ...state,
        notifications: {
          ...state.notifications,
          [payload.userConnectionId]: payload,
        },
      };
    // ********************
    case CLEAR_CHAT_NOTIFICATION:
      let notificationsCopy = {...state.notifications};
      delete notificationsCopy[payload];
      return {
        ...state,
        notifications: notificationsCopy,
      };
    // ********************
    default:
      return state;
  }
};

export default reducer;