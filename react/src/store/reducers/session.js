import { fetch } from "../../services/fetch";

// Action constants
const LOGIN_SESSION_USER = "session/loginSessionUser";
const LOGOUT_SESSION_USER = "session/logoutSessionUser";
const POST_SESSION_USER = "session/postSessionUser";
const GET_SESSION_USER = "session/getSessionUser";
const PATCH_SESSION_USER = "session/patchSessionUser";

// State template
const userTemplate = {
  id: null,
  firstName: null,
  lastName: null,
  email: null,
  shareLocation: null,
  coordLat: null,
  coordLong: null,
};

// Action creators
const loginSessionUserActionCreator = (payload) => ({
  type: LOGIN_SESSION_USER,
  payload,
});
const logoutSessionUserActionCreator = (payload) => ({
  type: LOGOUT_SESSION_USER,
  payload,
});
const postSessionUserActionCreator = (payload) => ({
  type: POST_SESSION_USER,
  payload,
});
const getSessionUserActionCreator = (payload) => ({
  type: GET_SESSION_USER,
  payload,
});
const patchSessionUserActionCreator = (payload) => ({
  type: PATCH_SESSION_USER,
  payload,
});

// Thunks

// TODO

// Reducer
const reducer = (state = { user: userTemplate }, { type, payload }) => {
  switch (type) {
    case LOGIN_SESSION_USER:
      return { session: { ...state.user, ...payload } };

    case LOGOUT_SESSION_USER:
      return { session: { ...state.user, ...payload } };

    case POST_SESSION_USER:
      return { session: { ...state.user, ...payload } };

    case GET_SESSION_USER:
      return { session: { ...state.user, ...payload } };

    case PATCH_SESSION_USER:
      return { session: { ...state.user, ...payload } };

    default:
      return state;
  }
};

export default reducer;
