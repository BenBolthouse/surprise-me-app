const model = {
  timestamp: null,
  csrfToken: null,
};

const reducer = (state = model, { type, payload }) => {
  switch (type) {
    case "session/POST":
      return { ...state, ...payload };

    case "session/GET":
      return { ...state, ...payload };

    case "session/GET_CSRF":
      return { ...state, ...payload };

    case "session/DELETE":
      return model;

    default:
      return state;
  }
};

export default reducer;
