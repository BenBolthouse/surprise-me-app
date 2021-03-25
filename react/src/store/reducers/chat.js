import { store } from "../../index";
import { fetch } from "../../services/fetch";

import * as connectionsActions from "./connections";

// Reducer template
const messageThreadsTemplate = {};

/**
 * Get the current client state.
 */
const getState = () => store.getState();

// ** «««««««««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»»»»»»»» **

const POST_MESSAGE = "chat/postMessage";
export const postMessage = ({ connId, body }) => async (dispatch) => {
  const storeState = getState();
  const message = {
    aggrType: "message",
    body,
    createdAt: new Date().toISOString(),
    deleted: false,
    id: null,
    sender: storeState.session.user,
    updated: false,
    userConnectionId: connId,
  };
  const client = storeState.session.socketClient;
  client.emit("chat_message", { message, roomId: connId });
  dispatch(
    ((payload) => ({
      type: POST_MESSAGE,
      payload,
    }))({ connId, message })
  );
  dispatch(getMessage({ connId, message }));
};

const POST_COMPOSER_INTERACTING = "chat/postComposerInteracting";
export const postComposerInteracting = (roomId, connId) => async (dispatch) => {
  const storeState = getState();
  const message = { roomId, connId, interacting: true };
  const client = storeState.session.socketClient;
  client.emit("composer_interacting", message);
  dispatch(
    ((payload) => ({
      type: POST_COMPOSER_INTERACTING,
      payload,
    }))({ roomId, connId })
  );
};

const DELETE_COMPOSER_INTERACTING = "chat/deleteComposerInteracting";
export const deleteComposerInteracting = (roomId) => async (dispatch) => {
  const storeState = getState();
  const message = { roomId, interacting: false };
  const client = storeState.session.socketClient;
  client.emit("composer_interacting", message);
  dispatch(
    ((payload) => ({
      type: DELETE_COMPOSER_INTERACTING,
      payload,
    }))({ roomId })
  );
};

const GET_COMPOSER_INTERACTING = "chat/getComposerInteracting";
export const getComposerInteracting = (payload) => ({
  type: GET_COMPOSER_INTERACTING,
  payload,
});

const GET_MESSAGES = "chat/getMessages";
export const getMessages = ({ connId, qty, offsetQty }) => async (dispatch) => {
  const url = `/api/connections/${connId}/messages/range?qty=${qty}&ofs=${offsetQty}`;
  const res = await fetch(url);
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: GET_MESSAGES,
      payload,
    }))({ connId, data })
  );
  return res;
};

const SPOOF_GET_MESSAGES = "chat/spoofGetMessages";
export const spoofGetMessages = (connId) => ({
  type: SPOOF_GET_MESSAGES,
  payload: connId,
});

const GET_MESSAGE = "chat/getMessage";
export const getMessage = ({ connId, message }) => ({
  type: GET_MESSAGE,
  payload: { connId, message },
});

// ** «««««««««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = messageThreadsTemplate, { type, payload }) => {
  switch (type) {
    // ********************
    case POST_MESSAGE:
      return {
        ...state,
        [payload.connId]: {
          ...state[payload.connId],
          interacting: false,
        },
      };
    // ********************
    case POST_COMPOSER_INTERACTING:
      return { ...state };
    // ********************
    case DELETE_COMPOSER_INTERACTING:
      return { ...state };
    // ********************
    case GET_COMPOSER_INTERACTING:
      return {
        ...state,
        [payload.connId]: {
          ...state[payload.connId],
          interacting: payload.interacting,
        },
      };
    // ********************
    case GET_MESSAGES:
      return {
        ...state,
        [payload.connId]: {
          lastMessage: null,
          interacting: false,
          messages: payload.data,
        },
      };
    // ********************
    case SPOOF_GET_MESSAGES:
      return {
        ...state,
        [payload]: {
          lastMessage: null,
          interacting: false,
          messages: [],
        },
      };
    // ********************
    case GET_MESSAGE:
      return {
        ...state,
        [payload.connId]: {
          lastMessage: payload.message,
          interacting: false,
          messages: [...state[payload.connId].messages, payload.message],
        },
      };
    // ********************
    default:
      return state;
  }
};

export default reducer;
