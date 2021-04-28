import { fetch } from "../../services/fetch";

// Action constants
const GET_X_CSRF_TOKEN = "security/getXCsrfToken";

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
  
  return res;
};

// Reducer
const reducer = (state = { security: securityTemplate }, { type, payload }) => {
  switch (type) {
    case GET_X_CSRF_TOKEN:
      return { ...state.security, ...payload };

    default:
      return state;
  }
};

export default reducer;
