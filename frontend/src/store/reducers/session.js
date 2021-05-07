import { fetch } from "../utilities/fetch";
import { Session } from "../models/Session";
import { requires, socket } from "../index";
import handler from "../utilities/error-handler";

const sessionManager = new Session("/api/v1/sessions", "/api/v1/csrf_token");

const GET_CSRF_TOKEN = "session ———————————> GET_CSRF_TOKEN";
const POST_SESSION = "session ———————————> POST_SESSION";
const GET_SESSION = "session ———————————> GET_SESSION";
const DELETE_SESSION = "session ———————————> DELETE_SESSION";

/**
 * Retrieves and saves a new CSRF security token.
 */
export const getCsrfToken = ()  => (dispatch) => handler(async () => {
  const { data } = await fetch(sessionManager.csrfEndpoint, { method: "GET" });

  dispatch(getCsrfTokenAction(data.token));
});

const getCsrfTokenAction = (payload) => ({ type: GET_CSRF_TOKEN, payload });

/**
 * Creates a new session and saves session user data to state.
 */
export const postSession = ({ email, password }) => (dispatch) => handler(async () => {
  requires.csrf();

  const body = { email, password };

  const { data } = await fetch(sessionManager.endpoint, { method: "POST", body });

  dispatch(postSessionAction(data));
});

const postSessionAction = (payload) => ({ type: POST_SESSION, payload });

/**
 * Gets new and saves session user data to state. Authentication required.
 */
export const getSession = () => (dispatch) => handler(async () => {
  const { data } = await fetch(sessionManager.endpoint, { method: "GET" });

  dispatch(getSessionAction(data));
});

const getSessionAction = (payload) => ({ type: GET_SESSION, payload });

/**
 * Removes session cookie and session user data from state. Also
 * disconnects the client socket.
 */
export const deleteSession = () => (dispatch) => handler(async () => {
  requires.csrf();
  socket.disconnect();

  await fetch(sessionManager.endpoint, { method: "DELETE" });

  dispatch(deleteSessionAction());
});

const deleteSessionAction = (payload) => ({ type: DELETE_SESSION, payload });

const reducer = (state = sessionManager.state(), { type, payload }) => {
  switch (type) {
    case GET_CSRF_TOKEN:
      sessionManager.csrfToken = payload;
      return sessionManager.state();

    case POST_SESSION:
      sessionManager.populateEntity(payload);
      return sessionManager.state();

    case GET_SESSION:
      sessionManager.populateEntity(payload);
      return sessionManager.state();

    default:
      return state;
  }
};

export default reducer;
