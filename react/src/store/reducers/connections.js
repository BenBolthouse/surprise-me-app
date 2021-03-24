import { fetch } from "../../services/fetch";
import { normalize } from "../../services/normalize";

// State template
const stateTemplate = {
  timestamp: null,
  established: {},
  pending: {},
  awaiting: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const GET_CONNECTIONS = "connections/getConnections";
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

const SPOOF_MESSAGE_CONNECTION = "chat/spoofMsgConnection";
export const spoofMessageConnection = (connId) => ({
  type: SPOOF_MESSAGE_CONNECTION,
  payload: connId,
});

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = stateTemplate, { type, payload }) => {
  switch (type) {
    // ********************
    case GET_CONNECTIONS:
      const estConnections = payload.filter((c) => {
        if (c.establishedAt !== null) return c;
        return false;
      });
      const pendingConnections = payload.filter((c) => {
        if (c.establishedAt === null) return c;
        return false;
      });
      return {
        ...state,
        timestamp: new Date().toISOString(),
        established: normalize(estConnections),
        pending: normalize(pendingConnections),
      };
    // ********************
    case SPOOF_MESSAGE_CONNECTION:
      return {
        ...state,
        established: {
          ...state.established,
          [payload]: {
            ...state.established[payload],
            lastMessage: {
              body: "",
              createdAt: new Date().toUTCString(),
              sender: {
                id: null,
              }
            }
          }
        }
      }
    default:
      return state;
  }
};

export default reducer;
