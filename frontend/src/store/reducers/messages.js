/** @module store/reducers/messages */

import { MessageManager } from "../models/Message";
import { api, handler, socket } from "../../index";
import { sessionManager } from "./session";

export const messagesManager = new MessageManager();

const LIMIT = 20;

// http actions
const POST_MESSAGE = "messages ——————————> POST_MESSAGE";
const GET_MESSAGES = "messages ——————————> GET_MESSAGES";
const PATCH_MESSAGE = "messages ——————————> UPDATE_MESSAGE";
const DELETE_MESSAGE = "messages ——————————> DELETE_MESSAGE";

// event actions
const RECEIVE_MESSAGE = "messages ——————————> RECEIVE_MESSAGE";
const AMEND_MESSAGE = "messages ——————————> AMEND_MESSAGE";
const DISCARD_MESSAGE = "messages ——————————> DISCARD_MESSAGE";

/**
 * Posts a new message.<br>
 * 
 * message:<br>
 * 
 * `{type, connectionId, body}`
 * @param {Object} message
 * @returns {true}
 */
export const postMessage = (message) => (dispatch) => handler(async () => {
  sessionManager.requireSession();
  socket.require();

  const action = (payload) => ({ type: POST_MESSAGE, payload });

  const { type, connectionId, body: msgBody } = message;

  const collection = messagesManager.getOrCreateMessagesCollection(connectionId);

  collection.offset ++;
  
  const body = { type, connectionId, body: msgBody }

  const { data } = await api.post(collection.endpoint, body);

  dispatch(action(data));

  return true;
});

/**
 * Gets new messages by offset limit.
 * @param {Number} connectionId
 * @returns {true}
 */
export const getMessages = (connectionId) => (dispatch) => handler(async () => {
  sessionManager.requireSession();
  socket.require();

  const action = (payload) => ({ type: GET_MESSAGES, payload });

  const collection = messagesManager.getOrCreateMessagesCollection(connectionId);

  const query = `?ofs=${collection.offset}&lim=${LIMIT}`;

  collection.offset += LIMIT;
  
  const endpoint = collection.endpoint + query;

  const { data } = await api.get(endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Updates a message.<br>
 * 
 * message:<br>
 * 
 * `{ connectionId, id, body }`
 * @param {object} message
 * @returns {true}
 */
export const patchMessage = (message) => (dispatch) => handler(async () => {
  sessionManager.requireSession();
  socket.require();

  const action = (payload) => ({ type: PATCH_MESSAGE, payload });
  
  const { connectionId, id, body: msgBody } = message;
  
  const collection = messagesManager.getOrCreateMessagesCollection(connectionId);
  
  const body = { body: msgBody }

  const endpoint = `${collection.endpoint}/${id}`
  
  const { data } = await api.patch(endpoint, body);

  dispatch(action(data));

  return true;
});

/**
 * Deletes a message.
 * 
 * message:<br>
 * 
 * `{ connectionId, id }`
 * @param {object} message
 * @returns {true}
 */
export const deleteMessage = (message) => (dispatch) => handler(async () => {
  sessionManager.requireSession();
  socket.require();

  const action = (payload) => ({ type: DELETE_MESSAGE, payload });
  
  const { connectionId, id } = message;

  const collection = messagesManager.getOrCreateMessagesCollection(connectionId);

  const endpoint = `${collection.endpoint}/${id}`
  
  const { data } = await api.delete(endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Socketio event receive new message.
 * @param {Object} payload Message object from event
 * @returns Redux action for reducer
 */
export const receiveMessage = ({ data }) => {
  const collection = messagesManager.getMessagesCollections(data.connection_id);

  collection.offset ++;
  
  return { type: RECEIVE_MESSAGE, payload: data }
};

/**
 * Socketio event receive updates to existing message.
 * @param {Object} payload Message object from event
 * @returns Redux action for reducer
 */
export const amendMessage = ({ data }) => {
  const collection = messagesManager.getMessagesCollections(data.connection_id);
  
  const message = collection.getMessage(data.messages[0].id);

  if (message) return { type: AMEND_MESSAGE, payload: data };

  return { type: "messages ——————————> NO_OP" }
};

/**
 * Socketio event delete and remove a message.
 * @param {Object} payload Message object from event
 * @returns Redux action for reducer
 */
export const discardMessage = ({ data }) => {
  const collection = messagesManager.getMessagesCollections(data.connection_id);
  
  const message = collection.getMessage(data.messages[0].id);

  if (message) return { type: DISCARD_MESSAGE, payload: data }

  return { type: "messages ——————————> NO_OP" }
};

const reducer = (state = messagesManager.copy(), { type, payload }) => {
  
  switch (type) {
    case POST_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case PATCH_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case GET_MESSAGES:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case DELETE_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case RECEIVE_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case AMEND_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    case DISCARD_MESSAGE:
      messagesManager.produceFrom(payload);
      return messagesManager.copy();

    default:
      return state;
  }
};

export default reducer;
