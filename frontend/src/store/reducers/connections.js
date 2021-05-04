import { fetch } from "../fetch";
import { Connection, ConnectionsCollection } from "../models/connection";

const connections = new ConnectionsCollection();

const POST_CONNECTION = "connections ———————> POST_CONNECTION";
const GET_CONNECTIONS = "connections ———————> GET_CONNECTIONS";
const APPROVE_CONNECTION = "connections ———————> APPROVE_CONNECTION";
const DENY_CONNECTION = "connections ———————> DENY_CONNECTION";
const LEAVE_CONNECTION = "connections ———————> DENY_CONNECTION";

export const postConnection = (id) => async (dispatch) => {
  const body = { "approver_id": id }
  const { data } = await fetch(connections.endpoint, { method: "POST", body });
  dispatch(() => ({ type: POST_CONNECTION, payload: data }));
  return true;
};

export const getConnections = () => async (dispatch) => {
  const { data } = await fetch(connections.endpoint, { method: "GET" });
  dispatch(() => ({ type: GET_CONNECTIONS, payload: data }));
  return true;
};

export const approveConnection = (id) => async (dispatch) => {
  const endpoint = `${connections.endpoint}/${id}/approve`;
  const { data } = await fetch(endpoint, { method: "PATCH" });
  dispatch(() => ({ type: APPROVE_CONNECTION, payload: data }));
  return true;
};

export const denyConnection = (id) => async (dispatch) => {
  const endpoint = `${connections.endpoint}/${id}/deny`;
  const { data } = await fetch(endpoint, { method: "PATCH" });
  dispatch(() => ({ type: DENY_CONNECTION, payload: data }));
  return true;
};

export const leaveConnection = (id) => async (dispatch) => {
  const endpoint = `${connections.endpoint}/${id}`;
  const { data } = await fetch(endpoint, { method: "DELETE" });
  dispatch(() => ({ type: LEAVE_CONNECTION, payload: data }));
  return true;
};

const reducer = (state = connections, { type, payload }) => {
  let connectionsCopy = { ...state };
  let connection;

  switch (type) {
    case POST_CONNECTION:
      connection = new Connection();
      connection.populate(payload);
      connectionsCopy.add(connection);
      return connectionsCopy;

    case GET_CONNECTIONS:
      connectionsCopy.populate(payload);
      return connectionsCopy;

    case APPROVE_CONNECTION:
      connection = connectionsCopy.filter(x => x.id === payload.id)
      connection.populate(payload);
      return connectionsCopy;

    case DENY_CONNECTION:
      connection = connectionsCopy.filter(x => x.id === payload.id)
      connection.populate(payload);
      return connectionsCopy;

    case LEAVE_CONNECTION:
      connection = connectionsCopy.filter(x => x.id === payload.id)
      connection.populate(payload);
      return connectionsCopy;

    default:
      return state;
  }
};

export default reducer;
