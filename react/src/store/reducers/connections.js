import _ from "lodash";

import { fetch } from "../../services/fetch";
import { normalize } from "../../services/normalize";

import { store } from "../../index";
import * as notificationsActions from "./notifications";

// State template
const stateTemplate = {
  datestamp: null,
  established: {},
  pending: {},
  awaiting: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const GET_CONNECTIONS = "connections/getConnections";
/**
 * Populate Redux established connections state on app
 * renders via request to the webserver.
 */
export const getConnections = () => async (dispatch) => {
  const res = await fetch("/api/connections");
  const { data } = res.data;
  dispatch(
    ((payload) => ({
      type: GET_CONNECTIONS,
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
  const established = { ...store.getState().connections.established };
  const normalized = Object.values(established);
  const request_body = {
    datestamp: established.datestamp,
    connections: normalized.map((connection) => ({
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
/**
 * Post a new message to Redux state and database.
 *
 * @param {*} object Contains required properties integer **connectionId** and string **body**.
 */
export const postConnectionMessage = ({ connectionId, body }) => async (
  dispatch
) => {
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
    case GET_CONNECTIONS:
      const estConnections = payload.filter(c => {
        if(c.establishedAt !== null) return c
      })
      const pendingConnections = payload.filter(c => {
        if(c.establishedAt === null) return c
      })
      return {
        ...state,
        datestamp: new Date().toISOString(),
        established: normalize(estConnections),
        pending: normalize(pendingConnections),
      };

    case UPDATE_ESTABLISHED_CONNECTIONS:
      if (!_.isEmpty(payload.connections)) {
        return {
          ...state,
          datestamp: new Date().toISOString(),
          established: {
            ...state.established,
            ...payload.connections,
          },
        };
      } else return state;

    case POST_CONNECTION_MESSAGE:
      stateCopy = { ...state };
      stateCopy.datestamp = new Date().toISOString();
      stateCopy.established[payload.userConnectionId].messages.push(
        payload
      );
      return stateCopy;

    default:
      return state;
  }
};

export default reducer;
