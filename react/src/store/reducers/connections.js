import { fetch } from "../../services/fetch";
import { normalize } from "../../services/normalize";

import { store } from '../../index'
import * as notificationsActions from "./notifications";

// State template
const stateTemplate = {
  established: {
    datestamp: null,
    connections: {},
  },
  pending: {},
  awaiting: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const GET_ESTABLISHED_CONNECTIONS = "connections/getEst...Connections";
/**
 * Populate Redux established connections state on app
 * renders via request to the webserver.
 */
export const getEstConnectionsOnLoad = () => async (dispatch) => {
  const res = await fetch("/api/connections/established");
  const { data } = res.data;
  data.connections = normalize(data.connections);
  dispatch(
    ((payload) => ({
      type: GET_ESTABLISHED_CONNECTIONS,
      payload,
    }))(data)
  );
  return res;
};

const UPDATE_ESTABLISHED_CONNECTIONS = "connections/updateEst...Connections";
/**
 * Check for updates to message counts on established
 * connections, best used on a periodic basis to keep the
 * client and webserver states synchronous.
 */
export const updateEstConnections = () => async (dispatch) => {
  const estConnCopy = {...store.getState().connections.established};
  const deNormConn = Object.values(estConnCopy.connections);
  const request_body = {
    datestamp: estConnCopy.datestamp,
    connections: deNormConn.map((connection) => ({
      id: connection.id,
      messagesCount: connection.messages.length,
    })),
  };
  const res = await fetch("/api/connections/established", {
    method: "POST",
    body: JSON.stringify(request_body),
  });
  const { data } = res.data;
  data.connections.forEach((connection) => {
    const fullName =
      connection.connectionFirstName + " " + connection.connectionLastName;
    dispatch(
      notificationsActions.setChatNotification({
        id: connection.id,
        message: `New message from ${fullName}`,
      })
    );
  });
  data.connections = normalize(data.connections);
  dispatch(
    ((payload) => ({
      type: UPDATE_ESTABLISHED_CONNECTIONS,
      payload,
    }))(data)
  );
  return res;
};

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = stateTemplate, { type, payload }) => {

  switch (type) {
    case GET_ESTABLISHED_CONNECTIONS:
      return {
        ...state,
        established: {
          datestamp: payload.datestamp,
          connections: payload.connections,
        },
      };

    case UPDATE_ESTABLISHED_CONNECTIONS:
      return {
        ...state,
        established: {
          datestamp: payload.datestamp,
          connections: {
            ...state.established.connections,
            ...payload.connections,
          },
        },
      };

    default:
      return state;
  }
};

export default reducer;
