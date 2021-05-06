import { Connection, ConnectionsCollection } from "../models/Connection";
import { fetch } from "../utilities/fetch";
import { requires } from "../index";

const connections = new ConnectionsCollection();

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
 *
 * @param {Object} config
 */
export const postConnection = ({ approverId }) => async (dispatch) => {
  requires.session();
  requires.csrf();

  const body = { approver_id: approverId };
  const { data } = await fetch(connections.endpoint, { method: "POST", body });

  dispatch(postConnectionAction(data));
};

const postConnectionAction = (payload) => ({ type: POST_CONNECTION, payload });

/**
 * Gets all connections and adds connections to related collections.
 */
export const getConnections = () => async (dispatch) => {
  connections.userId = requires.session().id;

  let { data } = await fetch(connections.endpoint, { method: "GET" });

  dispatch(getConnectionsAction(data));
};

const getConnectionsAction = (payload) => ({ type: GET_CONNECTIONS, payload });

/**
 * Approves a pending connection and moves the connection to the approved
 * collection.
 *
 * @param {Object} config
 */
export const approveConnection = ({ id }) => async (dispatch) => {
  requires.session();
  requires.csrf();

  const endpoint = `${connections.endpoint}/${id}/approve`;

  const { data } = await fetch(endpoint, { method: "PATCH" });
  dispatch(approveConnectionAction(data));

  return true;
};

const approveConnectionAction = (payload) => ({ type: APPROVE_CONNECTION, payload });

/**
 * Denies a pending connection and removes the connection from all
 * collections.
 *
 * @param {Object} config
 */
export const denyConnection = ({ id }) => async (dispatch) => {
  requires.session();
  requires.csrf();

  const endpoint = `${connections.endpoint}/${id}/deny`;

  const { data } = await fetch(endpoint, { method: "PATCH" });
  dispatch(denyConnectionAction(data));

  return true;
};

const denyConnectionAction = (payload) => ({ type: DENY_CONNECTION, payload });

/**
 * Leaves an approved connection and removes the connection from all
 * collections.
 *
 * @param {Object} config
 */
export const leaveConnection = ({ id }) => async (dispatch) => {
  requires.session();
  requires.csrf();

  const endpoint = `${connections.endpoint}/${id}`;

  const { data } = await fetch(endpoint, { method: "DELETE" });
  dispatch(leaveConnectionAction(data));

  return true;
};

const leaveConnectionAction = (payload) => ({ type: LEAVE_CONNECTION, payload });

/**
 * Socketio event other user composing.
 * 
 * @param {Object} payload Message object from event
 */
export const composingMessage = (payload) => ({ type: COMPOSING_MESSAGE, payload });

const reducer = (state = connections.state(), { type, payload }) => {
  let connection;

  switch (type) {
    case POST_CONNECTION:
      connection = new Connection(connections.endpoint);
      connection.populateEntity(payload);
      connections.addRequested(connection);
      return connections.state();

    case GET_CONNECTIONS:
      connections.populateCollection(payload);
      return connections.state();

    case APPROVE_CONNECTION:
      connection = connections.filter((x) => x.id === payload.id)[payload.id];
      connection.populateEntity(payload);
      connections.movePendingToApproved(payload);
      return connections.state();

    case DENY_CONNECTION:
      connections.removeFromAllCollections(payload);
      return connections.state();

    case LEAVE_CONNECTION:
      connections.removeFromAllCollections(payload);
      return connections.state();

    case COMPOSING_MESSAGE:
      connection = connections.filter((x) => x.id === payload.id)[payload.id];
      connection.populateEntity(payload);
      return connections.state();

    default:
      return state;
  }
};

export default reducer;
