import { fetch } from "../utilities/fetch";
import { MessageManager } from "../models/Message";
import { requires, socket } from "../index";

const messagesManager = new MessageManager();

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
 * Posts a new message.
 * 
 * @param {Object} config
 */
export const postMessage = ({ connectionId, type, body: msgBody }) => async (dispatch) => {
  requires.session();
  requires.csrf();
  socket.require();

  const collection = messagesManager.getOrCreateMessageCollection(connectionId);

  collection.offset ++;
  
  const body = {
    type,
    connection_id: connectionId,
    body: msgBody,
  }

  const { data } = await fetch(collection.endpoint, { method: "POST", body });

  dispatch(postMessageAction(data));
};

const postMessageAction = (payload) => ({ type: POST_MESSAGE, payload });

/**
 * Gets new messages by offset limit.
 * 
 * @param {Object} config
 */
export const getMessages = ({ connectionId }) => async (dispatch) => {
  requires.session().id;

  const collection = messagesManager.getOrCreateMessageCollection(connectionId);

  const query = `?ofs=${collection.offset}&lim=${LIMIT}`;

  collection.offset += LIMIT;
  
  const endpoint = collection.endpoint + query;

  const { data } = await fetch(endpoint, { method: "GET" });

  dispatch(getMessagesAction(data));
};

const getMessagesAction = (payload) => ({ type: GET_MESSAGES, payload });

/**
 * Updates a message.
 * 
 * @param {Object} config
 */
export const patchMessage = ({ connectionId, id, type, body: msgBody }) => async (dispatch) => {
  requires.session();
  requires.csrf();
  socket.require();

  const collection = messagesManager.getOrCreateMessageCollection(connectionId);
  
  const body = {
    type,
    body: msgBody,
    updated_at: new Date().toISOString(),
  }

  const endpoint = `${collection.endpoint}/${id}`
  
  const { data } = await fetch(endpoint, { method: "PATCH", body });

  dispatch(patchMessageAction(data));
};

const patchMessageAction = (payload) => ({ type: PATCH_MESSAGE, payload });

/**
 * Deletes a message.
 * 
 * @param {Object} config
 */
export const deleteMessage = ({ connectionId, id }) => async (dispatch) => {
  requires.session();
  requires.csrf();
  socket.require();

  const collection = messagesManager.getOrCreateMessageCollection(connectionId);

  const endpoint = `${collection.endpoint}/${id}`
  
  const { data } = await fetch(endpoint, { method: "DELETE" });

  dispatch(deleteMessageAction(data));
};

const deleteMessageAction = (payload) => ({ type: DELETE_MESSAGE, payload });

/**
 * Socketio event receive new message.
 * 
 * @param {Object} payload Message object from event
 */
export const receiveMessage = ({ data }) => {
  const collection = messagesManager.getMessageCollection(data.connection_id);

  collection.offset ++;
  
  return { type: RECEIVE_MESSAGE, payload: data }
};

/**
 * Socketio event receive updates to existing message.
 * 
 * @param {Object} payload Message object from event
 */
export const amendMessage = ({ data }) => {
  const collection = messagesManager.getMessageCollection(data.connection_id);
  
  const message = collection ? collection.getMessage(data.messages[0].id) : null;

  if (message) {
    return { type: AMEND_MESSAGE, payload: data }
  }

  return { type: "messages ——————————> NO_OP" }
};

/**
 * Socketio event delete and remove a message.
 * 
 * @param {Object} payload Message object from event
 */
export const discardMessage = ({ data }) => {
  const collection = messagesManager.getMessageCollection(data.connection_id);
  
  const message = collection ? collection.getMessage(data.messages[0].id) : null;

  if (message) {
    return { type: DISCARD_MESSAGE, payload: data }
  }

  return { type: "messages ——————————> NO_OP" }
};

const reducer = (state = messagesManager.state(), { type, payload }) => {
  
  switch (type) {
    case POST_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case PATCH_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case GET_MESSAGES:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case DELETE_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case RECEIVE_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case AMEND_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case DISCARD_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    default:
      return state;
  }
};

export default reducer;
