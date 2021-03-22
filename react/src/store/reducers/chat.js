import { store } from "../../index";
import { fetch } from "../../services/fetch";

import * as sessionActions from "./session";

// Reducer template
const messageThreadsTemplate = {};

/**
 * Get the current state.
 */
const getState = () => store.getState();

// ** «««««««««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»»»»»»»» **

const POST_MESSAGE = "chat/postMessage";

export const postMessage = ({ connId, body }) => async (dispatch) => {
  const storeState = getState();
  const message = {
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
};

const POST_COMPOSER_INTERACTING = "chat/postComposerInteracting";

export const postComposerInteracting = (connId) => ({
  type: POST_COMPOSER_INTERACTING,
  payload: connId,
});

const DELETE_COMPOSER_INTERACTING = "chat/deleteComposerInteracting";

export const deleteComposerInteracting = (connId) => ({
  type: DELETE_COMPOSER_INTERACTING,
  payload: connId,
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

const GET_MESSAGE = "chat/getMessage";

export const getMessage = ({connId, message}) => ({
  type: GET_MESSAGE,
  payload: {connId, message},
});

// ** «««««««««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = messageThreadsTemplate, { type, payload }) => {
  switch (type) {
    case POST_MESSAGE:
      return {
        ...state,
        [payload.connId]: {
          interacting: false,
          messages: [
            ...state[payload.connId].messages,
            payload.message,
          ]
        },
      };

    case POST_COMPOSER_INTERACTING:
      return {
        ...state,
        [payload]: {
          ...state[payload],
          interacting: true,
        },
      };

    case DELETE_COMPOSER_INTERACTING:
      return {
        ...state,
        [payload]: {
          ...state[payload],
          interacting: false,
        },
      };

    case GET_MESSAGES:
      return {
        ...state,
        [payload.connId]: {
          interacting: false,
          messages: payload.data,
        },
      };
    
    case GET_MESSAGE:
      return {
        ...state,
        [payload.connId]: {
          interacting: false,
          messages: [
            ...state[payload.connId].messages,
            payload.message,
          ]
        },
      };

    default:
      return state;
  }
};

export default reducer;
