import { post, get, patch, destroy } from "../../utilities";
import { socketIoClient } from "../socketIoClient";
import { store } from "../.."

export const session = {
  post: (props) => async (dispatch) => {
    const { data, status } = await post("/api/v1/sessions", props);
    return dispatch({ type: "session/POST", payload: { data, status } });
  },
  get: () => async (dispatch) => {
    const { data, status } = await get("/api/v1/sessions");
    return dispatch({ type: "session/GET", payload: { data, status } });
  },
  getCsrf: () => async (dispatch) => {
    const { data, status } = await get("/api/v1/sessions/csrf");
    return dispatch({ type: "session/GET_CSRF", payload: { data, status } });
  },
  delete: () => async (dispatch) => {
    await destroy("/api/v1/sessions");
    return dispatch({ type: "session/DELETE" });
  },
};

export const user = {
  post: (props) => async (dispatch) => {
    const { data, status } = await post("/api/v1/users", props);
    return dispatch({ type: "user/POST", payload: { data, status } });
  },
  postEmailUnique: (props) => async (dispatch) => {
    const { data, status } = await post("/api/v1/users/email_unique", props);
    return dispatch({ type: "user/POST_EMAIL_UNIQUE", payload: { data, status } });
  },
  get: () => async (dispatch) => {
    const { data, status } = await get("/api/v1/users");
    return dispatch({ type: "user/GET", payload: { data, status } });
  },
  patch: (props) => async (dispatch) => {
    const { data, status } = await patch("/api/v1/users", props);
    return dispatch({ type: "user/PATCH", payload: { data, status } });
  },
  patchEmail: (email) => async (dispatch) => {
    const { data, status } = await patch("/api/v1/users/email", email);
    return dispatch({ type: "user/PATCH_EMAIL", payload: { data, status } });
  },
  patchPassword: (password) => async (dispatch) => {
    const { data, status } = await patch("/api/v1/users/password", password);
    return dispatch({ type: "user/PATCH_PASSWORD", payload: { data, status } });
  },
  delete: () => async (dispatch) => {
    await destroy("/api/v1/users");
    return dispatch({ type: "user/DELETE" });
  },
};

export const connections = {
  post: (approverId) => async (dispatch) => {
    const { data, status } = await post("/api/v1/connections", approverId);
    return dispatch({ type: "connections/POST", payload: { data, status } });
  },
  get: () => async (dispatch) => {
    const { data, status } = await get("/api/v1/connections");
    return dispatch({
      type: "connections/GET",
      payload: {
        data: { userId: store.getState().user.id, connections: data },
        status,
      },
    });
  },
  approve: (id) => async (dispatch) => {
    const { data, status } = await patch("/api/v1/connections" + `/${id}/approve`);
    return dispatch({ type: `connections/APPROVE`, payload: { data, status } });
  },
  deny: (id) => async (dispatch) => {
    const { data, status } = await patch("/api/v1/connections" + `/${id}/deny`);
    return dispatch({ type: `connections/DENY`, payload: { data, status } });
  },
  leave: (id) => async (dispatch) => {
    const { data, status } = await destroy("/api/v1/connections" + `/${id}`);
    return dispatch({ type: `connections/LEAVE`, payload: { data, status } });
  },
};

export const messages = {
  post: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages`;
    const { data, status } = await post(url, props);
    return dispatch({ type: "messages/POST", payload: { data, status } });
  },
  get: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages`;
    const { data, status } = await get(url);
    return dispatch({ type: "messages/GET", payload: { data, status } });
  },
  patch: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages/${props.id}`;
    const { data, status } = await patch(url, props);
    return dispatch({ type: `messages/PATCH`, payload: { data, status } });
  },
  delete: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages/${props.id}`;
    const { data, status } = await destroy(url);
    return dispatch({ type: `messages/DELETE`, payload: { data, status } });
  },
};
socketIoClient.on("messages/events/post", (payload) => ({
  type: "messages/events/POST",
  payload,
}));
socketIoClient.on("messages/events/patch", (payload) => ({
  type: "messages/events/PATCH",
  payload,
}));
socketIoClient.on("messages/events/delete", (payload) => ({
  type: "messages/events/DELETE",
  payload,
}));

export const notifications = {
  get: () => async (dispatch) => {
    const url = `/api/v1/notifications`;
    const { data, status } = await get(url);
    return dispatch({ type: `notifications/GET`, payload: { data, status } });
  },
  bell: {
    dismiss: (idArray) => async (dispatch) => {
      const url = `/api/v1/notifications/dismiss`;
      const { data, status } = await patch(url, { ids: idArray });
      return dispatch({ type: `notifications/bell/DISMISS`, payload: { data, status } });
    },
  },
  card: {
    create: (props) => ({
      type: "notifications/card/CREATE",
      payload: props,
    }),
    dismiss: (id) => ({
      type: "notifications/card/DISMISS",
      payload: id,
    }),
  },
  message: {
    dismiss: (idArray) => async (dispatch) => {
      const url = `/api/v1/notifications/dismiss`;
      const { data, status } = await patch(url, { ids: idArray });
      return dispatch({ type: `notifications/message/DISMISS`, payload: { data, status } });
    },
  },
  popup: {
    create: (props) => ({
      type: "notifications/popup/CREATE",
      payload: { data: props },
    }),
  },
};

socketIoClient.on("notifications/bell/post", (payload) => ({
  type: "notifications/bell/POST",
  payload,
}));
socketIoClient.on("notifications/message/post", (payload) => ({
  type: "notifications/message/POST",
  payload,
}));
