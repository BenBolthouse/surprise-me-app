import _ from "lodash";

import { fetch } from "../../services/fetch";
import { normalize } from "../../services/normalize";

import { store } from "../../index";
import * as notificationsActions from "./notifications";

// State template
const stateTemplate = {
  datestamp: null,
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
  const estConnCopy = { ...store.getState().connections.established };
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

const POST_CONNECTION_MESSAGE = "connections/postConnectionMessage";

export const postConnectionMessage = ({
  connectionId,
  body,
}) => async (dispatch) => {
  const request_body = {
    body,
  };
  const res = await fetch(`/api/connections/${connectionId}/messages`, {
    method: "POST",
    body: JSON.stringify(request_body),
  });
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: POST_CONNECTION_MESSAGE,
      payload,
    }))(data)
  );
  return data;
};

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = stateTemplate, { type, payload }) => {
  let stateCopy;

  switch (type) {
    case GET_ESTABLISHED_CONNECTIONS:
      return {
        ...state,
        datestamp: new Date(),
        established: {
          datestamp: payload.datestamp,
          connections: payload.connections,
        },
      };

    case UPDATE_ESTABLISHED_CONNECTIONS:
      if(!_.isEmpty(payload.connections)) {
        return {
          ...state,
          established: {
            connections: {
              ...state.established.connections,
              ...payload.connections,
            },
          },
        };
      }
      else return state;

    case POST_CONNECTION_MESSAGE:
      stateCopy = { ...state };
      stateCopy.established.connections[payload.userConnectionId].messages.push(
        payload
      );
      return stateCopy;

    default:
      return state;
  }
};

export default reducer;
