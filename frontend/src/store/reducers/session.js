import { fetch } from "../fetch";
import { Session } from "../models/session";

const session = new Session("/api/v1/sessions");

const GET_CSRF_TOKEN = "session ———————————> GET_CSRF_TOKEN";
const POST_SESSION = "session ———————————> POST_SESSION";
// const GET_SESSION = "session ———————————> GET_SESSION";
// const DELETE_SESSION = "session ———————————> DELETE_SESSION";

export const getCsrfToken = () => async (dispatch) => {
  const { data } = await fetch(session.endpoint, { method: "GET" });
  dispatch(() => ({ type: GET_CSRF_TOKEN, payload: data }));
  return true;
};

export const postSession = (email, password) => async (dispatch) => {
  const body = { email, password };
  const { data } = await fetch(session.endpoint, { method: "POST", body });
  dispatch(() => ({ type: POST_SESSION, payload: data }));
  return true;
};

const reducer = (state = session, { type, payload }) => {
  let sessionCopy = { ...state };

  switch (type) {
    case GET_CSRF_TOKEN:
      sessionCopy.setCsrfToken(payload);
      return sessionCopy;
    
    case POST_SESSION:
      sessionCopy.populate(payload);
      return sessionCopy;

    default:
      return state;
  }
};

export default reducer;
