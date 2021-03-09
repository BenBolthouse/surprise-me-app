import { fetch } from "../../services/fetch";

// Action constants
const GET_X_CSRF_TOKEN = "session/getXCsrfToken";

// State template
const securityTemplate = {
  xCsrfToken: null,
};

// Action creators
const getXCsrfTokenActionCreator = (payload) => ({
  type: GET_X_CSRF_TOKEN,
  payload: {
    xCsrfToken: payload.token
  },
});

// Thunks
export const getXCsrfToken = () => async (dispatch) => {
  const res = await fetch("/api/csrf");
  const { data } = res.data;

  dispatch(getXCsrfTokenActionCreator(data));
  
  return data;
};

// Reducer
const reducer = (state = { security: securityTemplate }, { type, payload }) => {
  switch (type) {
    case GET_X_CSRF_TOKEN:
      return { security: { ...state.security, ...payload } };

    default:
      return state;
  }
};

export default reducer;
