import { fetch } from "../utilities/fetch";
import { MessageManager } from "../models/Message";
import { requires, socket } from "../index";

const messagesManager = new MessageManager();

const LIMIT = 20;

const POST_MESSAGE = "messages ——————————> POST_MESSAGE"
const GET_MESSAGES = "messages ——————————> GET_MESSAGES";
const PATCH_MESSAGE = "messages ——————————> UPDATE_MESSAGE";
const RECEIVE_MESSAGE = "messages ——————————> RECEIVE_MESSAGE"
const AMEND_MESSAGE = "messages ——————————> RECEIVE_MESSAGE"
// const UPDATE_MESSAGE = "messages ——————————> UPDATE_MESSAGE"
// const DELETE_MESSAGE = "messages ——————————> DELETE_MESSAGE"
// const COMPOSE_MESSAGE = "messages ——————————> COMPOSE_MESSAGE"
// const ABANDON_MESSAGE = "messages ——————————> ABANDON_MESSAGE"

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
 * Socketio event receive new message.
 * 
 * @param {Object} payload Message object from event
 */
export const receiveMessage = ({ data }) => {
  const collection = messagesManager.getOrCreateMessageCollection(data.connection_id);

  collection.offset ++;
  
  return { type: RECEIVE_MESSAGE, payload: data }
};

/**
 * Socketio event receive updates to existing message.
 * 
 * @param {Object} payload Message object from event
 */
export const amendMessage = ({ data }) => ({ type: AMEND_MESSAGE, payload: data });

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

const reducer = (state = messagesManager.state(), { type, payload }) => {
  switch (type) {
    case POST_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case PATCH_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case RECEIVE_MESSAGE:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    case GET_MESSAGES:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    default:
      return state;
  }
};

export default reducer;
