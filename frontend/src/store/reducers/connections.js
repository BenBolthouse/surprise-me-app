/** @module store/reducers/connections */

import { Connection, ConnectionsCollection } from "../models/Connection";
import { api, handler } from "../../index";
import { sessionManager } from "./session";

export const connections = new ConnectionsCollection();

// http actions
const POST_CONNECTION = "connections ———————> POST_CONNECTION";
const GET_CONNECTIONS = "connections ———————> GET_CONNECTIONS";
const APPROVE_CONNECTION = "connections ———————> APPROVE_CONNECTION";
const DENY_CONNECTION = "connections ———————> DENY_CONNECTION";
const LEAVE_CONNECTION = "connections ———————> LEAVE_CONNECTION";

// event actions
const COMPOSING_MESSAGE = "connections ———————> COMPOSING_MESSAGE";

/**
 * Posts a new connection and adds the connection to requested collection.
 * @param {object} config
 * @returns {true}
 */
export const postConnection = (id) => (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const action = (payload) => ({ type: POST_CONNECTION, payload });

  const body = { approverId: id };

  const { data } = await api.post(connections.endpoint, body);

  dispatch(action(data));

  return true;
});

/**
 * Gets all connections and adds connections to related collections.
 * @returns {true}
 */
export const getConnections = () => (dispatch) => handler(async () => {
  const action = (payload) => ({ type: GET_CONNECTIONS, payload });

  connections.userId = sessionManager.requireSession().id;

  const { data } = await api.get(connections.endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Approves a pending connection and moves the connection to the approved
 * collection.
 * @param {object} id
 * @returns {true}
 */
export const approveConnection = (id) => (dispatch) => handler(async () => {
  sessionManager.requireSession();
  
  const action = (payload) => ({ type: APPROVE_CONNECTION, payload });

  const endpoint = `${connections.endpoint}/${id}/approve`;

  const { data } = await api.patch(endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Denies a pending connection and removes the connection from all
 * collections.
 * @param {Number} id
 * @returns {true}
 */
export const denyConnection = (id) => async (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const action = (payload) => ({ type: DENY_CONNECTION, payload });

  const endpoint = `${connections.endpoint}/${id}/deny`;

  const { data } = await api.patch(endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Leaves an approved connection and removes the connection from all
 * collections.
 * @param {Number} id
 * @returns {true}
 */
export const leaveConnection = (id) => async (dispatch) => handler(async () => {
  sessionManager.requireSession();

  const action = (payload) => ({ type: LEAVE_CONNECTION, payload });

  const endpoint = `${connections.endpoint}/${id}`;

  const { data } = await api.delete(endpoint);

  dispatch(action(data));

  return true;
});


/**
 * Socketio event other user composing.
 * @param {object} payload Message object from event
 */
export const composingMessage = (payload) => ({ type: COMPOSING_MESSAGE, payload });

const reducer = (state = connections.copy(), { type, payload }) => {
  let connection;

  switch (type) {
    case POST_CONNECTION:
      connection = new Connection(connections.endpoint);
      connection.produceEntityFrom(payload);
      connections.addRequested(connection);
      return connections.copy();

    case GET_CONNECTIONS:
      connections.produceFrom(payload);
      return connections.copy();

    case APPROVE_CONNECTION:
      connection = connections.filter((x) => x.id === payload.id);
      connection.produceEntityFrom(payload);
      connections.movePendingToApproved(payload);
      return connections.copy();

    case DENY_CONNECTION:
      connections.removeFromAllCollections(payload);
      return connections.copy();

    case LEAVE_CONNECTION:
      connections.removeFromAllCollections(payload);
      return connections.copy();

    case COMPOSING_MESSAGE:
      connection = connections.filter((x) => x.id === payload.id);
      connection.produceEntityFrom(payload);
      return connections.copy();

    default:
      return state;
  }
};

export default reducer;
