import { Session } from "../models/Session";
import { api, handler, socket } from "../../index";

export const sessionManager = new Session("/api/v1/sessions", "/api/v1/csrf_token");

const GET_CSRF_TOKEN = "session ———————————> GET_CSRF_TOKEN";

// session management actions
const SIGN_IN = "session ———————————> SIGN_IN";
const SIGN_OUT = "session ———————————> SIGN_OUT";
const FETCH = "session ———————————> FETCH";

// user management actions
const VALIDATE = "session ———————————> VALIDATE";
const RESET_VALIDATION = "session ———————————> RESET_VALIDATION";
const POST_PATCH = "session ———————————> POST_PATCH";

/**
 * Retrieves a new CSRF token.
 * @returns {true}
 */
export const getCsrfToken = () => (dispatch) => handler(async () => {
  const action = (payload) => ({ type: GET_CSRF_TOKEN, payload });

  const { data } = await api.get(sessionManager.csrfEndpoint);

  api.setCsrfToken(data.token);

  dispatch(action(data.token));
});

/**
 * Retrieves a new session cookie for authentication and produces the
 * session state with user data.<br>
 * 
 * signIn:<br>
 * 
 * `{email, password}`
 * @param {object} signIn
 * @returns {type}
 */
export const signIn = (signIn) => (dispatch) => handler(async () => {
  const action = (payload) => ({ type: SIGN_IN, payload });

  const { data } = await api.post(sessionManager.endpoint, signIn);

  dispatch(action(data));

  return true;
});

/**
 * Gets new and saves session user data to state. Authentication required.
 * @returns {true}
 */
export const getSession = () => (dispatch) => handler(async () => {
  const action = (payload) => ({ type: FETCH, payload });
  
  const { data } = await api.get(sessionManager.endpoint);

  dispatch(action(data));

  return true;
});

/**
 * Removes session cookie and session user data from state. Also
 * disconnects the client socket.
 * @returns {true}
 */
export const logOut = () => (dispatch) => handler(async () => {
  const action = () => ({ type: SIGN_OUT });
  
  socket.disconnect();

  await api.delete(sessionManager.endpoint);

  dispatch(action());

  return true;
});

/**
 * Runs validation on the session object with the provided props.<br>
 * 
 * user:<br>
 * 
 * `{ firstName, lastName, email, password, confirmPassword }`
 * @param {object} user
 * @returns Redux action for reducer
 */
export const updateUserValidate = (user) => ({
  type: VALIDATE,
  payload: user,
});

/**
 * Resets the state of validation for the session object.
 * @returns Redux action for reducer
 */
export const resetUserValidate = () => ({
  type: RESET_VALIDATION,
  payload: {},
});

/**
 * Creates an application user or updates an existing user. Returns false
 * if session user validation fails.
 * @returns {true}
 */
export const postPatchUser = (user) => (dispatch) => handler(async () => {
  const action = (payload) => ({ type: FETCH, payload });
  
  sessionManager.produceEntityFrom(user);

  if (!sessionManager.validationResult) return false;
  
  const { data } = await api.post(sessionManager.endpoint, user);
  
  dispatch(action(data));

  return true;
})

const reducer = (state = sessionManager.copy(), { type, payload }) => {
  switch (type) {
    case GET_CSRF_TOKEN:
      sessionManager.csrfToken = payload;
      return sessionManager.copy();

    case SIGN_IN:
      sessionManager.produceEntityFrom(payload);
      return sessionManager.copy();

    case FETCH:
      sessionManager.produceEntityFrom(payload);
      return sessionManager.copy();

    case VALIDATE:
      sessionManager.setValidationErrorsVisible(true);
      sessionManager.produceEntityFrom(payload);
      return sessionManager.copy();

    case RESET_VALIDATION:
      sessionManager.resetValidation();
      sessionManager.produceEntityFrom(payload);
      return sessionManager.copy();

    case POST_PATCH:
      sessionManager.produceEntityFrom(payload);
      return sessionManager.copy();

    default:
      return state;
  }
};

export default reducer;
