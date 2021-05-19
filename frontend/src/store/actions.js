import * as req from "./fetch";
import socketClient from "./socketio";

export const session = {
  post: (props) => async (dispatch) => {
    const data = await req.post("/api/v1/sessions", props);
    return dispatch({ type: "session/POST", payload: data });
  },
  get: () => async (dispatch) => {
    const data = await req.get("/api/v1/sessions");
    return dispatch({ type: "session/GET", payload: data });
  },
  getCsrf: () => async (dispatch) => {
    const data = await req.get("/api/v1/sessions/csrf");
    return dispatch({ type: "session/GET_CSRF", payload: data });
  },
  delete: () => async (dispatch) => {
    await req.destroy("/api/v1/sessions");
    return dispatch({ type: "session/DELETE" });
  },
};

export const user = {
  post: (props) => async (dispatch) => {
    const data = await req.post("/api/v1/users", props);
    return dispatch({ type: "user/POST", payload: data });
  },
  get: () => async (dispatch) => {
    const data = await req.get("/api/v1/users");
    return dispatch({ type: "user/GET", payload: data });
  },
  patch: (props) => async (dispatch) => {
    const data = await req.patch("/api/v1/users", props);
    return dispatch({ type: "user/PATCH", payload: data });
  },
  patchEmail: (email) => async (dispatch) => {
    const data = await req.patch("/api/v1/users/email", email);
    return dispatch({ type: "user/PATCH_EMAIL", payload: data });
  },
  patchPassword: (password) => async (dispatch) => {
    const data = await req.patch("/api/v1/users/password", password);
    return dispatch({ type: "user/PATCH_PASSWORD", payload: data });
  },
  delete: () => async (dispatch) => {
    await req.destroy("/api/v1/users");
    return dispatch({ type: "user/DELETE" });
  },
};

export const connections = {
  _url: "/api/v1/connections",

  post: (approverId) => async (dispatch) => {
    const data = await req.post(connections._url, approverId);
    return dispatch({ type: "connections/POST", payload: data });
  },
  get: () => async (dispatch) => {
    const data = await req.get(connections._url);
    return dispatch({ type: "connections/GET", payload: data });
  },
  approve: (id) => async (dispatch) => {
    const data = await req.patch(connections._url + `/${id}/approve`);
    return dispatch({ type: `connections/${id}/APPROVE`, payload: data });
  },
  deny: (id) => async (dispatch) => {
    const data = await req.patch(connections._url + `/${id}/deny`);
    return dispatch({ type: `connections/${id}/DENY`, payload: data });
  },
  leave: (id) => async (dispatch) => {
    const data = await req.destroy(connections._url + `/${id}`);
    return dispatch({ type: `connections/${id}/LEAVE`, payload: data });
  },
};

export const messages = {
  post: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages`;
    const data = await req.post(url, props);
    return dispatch({ type: "messages/POST", payload: data });
  },
  get: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages`;
    const data = await req.get(url);
    return dispatch({ type: "messages/GET", payload: data });
  },
  patch: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages/${props.id}`;
    const data = await req.patch(url, props);
    return dispatch({ type: `messages/PATCH`, payload: data });
  },
  delete: (props) => async (dispatch) => {
    const url = `/api/v1/connections/${props.connectionId}/messages/${props.id}`;
    const data = await req.destroy(url);
    return dispatch({ type: `messages/DELETE`, payload: data });
  },
};
socketClient.on("messages/events/post", (payload) => ({
  type: "messages/events/POST",
  payload,
}));
socketClient.on("messages/events/patch", (payload) => ({
  type: "messages/events/PATCH",
  payload,
}));
socketClient.on("messages/events/delete", (payload) => ({
  type: "messages/events/DELETE",
  payload,
}));

export const notifications = {
  get: () => async (dispatch) => {
    const url = `/api/v1/notifications`;
    const data = await req.get(url);
    return dispatch({ type: `notifications/GET`, payload: data });
  },
  bell: {
    dismiss: (idArray) => async (dispatch) => {
      const url = `/api/v1/notifications/dismiss`;
      const data = await req.patch(url, { ids: idArray });
      return dispatch({ type: `notifications/bell/DISMISS`, payload: data });
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
      const data = await req.patch(url, { ids: idArray });
      return dispatch({ type: `notifications/message/DISMISS`, payload: data });
    },
  },
  popup: {
    create: (props) => ({
      type: "notifications/popup/CREATE",
      payload: props,
    }),
  },
};

socketClient.on("notifications/bell/post", (payload) => ({
  type: "notifications/bell/POST",
  payload,
}));
socketClient.on("notifications/message/post", (payload) => ({
  type: "notifications/message/POST",
  payload,
}));
