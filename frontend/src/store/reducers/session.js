import { fetch } from "../fetch";
import { Session } from "../models/session";
import { requireCsrf } from "../require";

const session = new Session("/api/v1/sessions", "/api/v1/csrf_token");

const GET_CSRF_TOKEN = "session ———————————> GET_CSRF_TOKEN";
const POST_SESSION = "session ———————————> POST_SESSION";
const GET_SESSION = "session ———————————> GET_SESSION";
const DELETE_SESSION = "session ———————————> DELETE_SESSION";

export const getCsrfToken = () => async (dispatch) => {
  const { data } = await fetch(session.csrfEndpoint, { method: "GET" });
  dispatch(getCsrfTokenAction(data));
};

const getCsrfTokenAction = (payload) => ({
  type: GET_CSRF_TOKEN,
  payload,
});

export const postSession = ({ email, password }) => async (dispatch) => {
  requireCsrf();

  const body = { email, password };
  const { data } = await fetch(session.endpoint, { method: "POST", body });

  dispatch(postSessionAction(data));
};

const postSessionAction = (payload) => ({
  type: POST_SESSION,
  payload,
});

export const getSession = () => async (dispatch) => {
  const { data } = await fetch(session.endpoint, { method: "GET" });

  dispatch(getSessionAction(data));
};

const getSessionAction = (payload) => ({
  type: GET_SESSION,
  payload,
});

export const deleteSession = () => async (dispatch) => {
  requireCsrf();
  
  await fetch(session.endpoint, { method: "DELETE" });

  dispatch(deleteSessionAction());
};

const deleteSessionAction = (payload) => ({
  type: DELETE_SESSION,
  payload,
});

const reducer = (state = session.state(), { type, payload }) => {
  switch (type) {
    case GET_CSRF_TOKEN:
      session.setCsrfToken(payload);
      return session.state();

    case POST_SESSION:
      session.populateEntity(payload);
      return session.state();

    case GET_SESSION:
      session.populateEntity(payload);
      return session.state();

    default:
      return state;
  }
};

export default reducer;
