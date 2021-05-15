import * as api from "../../fetch";
import connectionsManager from "../models/connection.model";

export const getConnections = () => async (dispatch) => {
  const { data } = await api.get("/api/v1/connections");

  const payload = connectionsManager.divvy(data);

  return dispatch({ type: "connections/GET_CONNECTIONS", payload });
};

export const requestConnection = (approverId) => async (dispatch) => {
  let payload;

  const body = {
    approverId,
  };

  const { data } = await api.post("/api/v1/connections", body);

  if (data) {
    payload = connectionsManager
      .collection("requested_connections")
      .createEntity(data);
  }

  return dispatch({ type: "connections/GET_CONNECTIONS", payload });
};

export const approveConnection = (props) => async (dispatch) => {
  let payload;

  const url = `/api/v1/connections/${props.id}/approve`;

  const { data } = await api.patch(url);

  if (data) {
    payload = connectionsManager
      .collection("pending_connections")
      .entity((x) => x.id === props.id)
      .update(data);

    connectionsManager.moveToCollection(
      data,
      "pending_connections",
      "approved_connections"
    );
  }

  return dispatch({ type: "connections/GET_CONNECTIONS", payload });
};

export const denyConnection = (props) => async (dispatch) => {
  const url = `/api/v1/connections/${props.id}/deny`;

  const { data } = await api.patch(url);

  if (data) {
    connectionsManager.removeFromCollections(data);
  }

  return dispatch({ type: "connections/DENY_CONNECTION" });
};

export const leaveConnection = (props) => async (dispatch) => {
  let payload;

  const url = "/api/v1/connections/" + props.id;

  const { data } = await api.destroy(url);

  if (data) {
    connectionsManager.removeFromCollections(data);
  }

  return dispatch({ type: "connections/GET_CONNECTIONS", payload });
};

const reducer = (_state, { type }) => {
  switch (type) {
    default:
      return connectionsManager.return();
  }
};

export default reducer;
