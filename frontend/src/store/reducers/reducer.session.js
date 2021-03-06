const model = {
  timestamp: null,
  csrfToken: null,
};

export const sessionReducer = (state = model, { type, payload }) => {
  const data = payload ? payload.data : null;

  switch (type) {
    case "session/POST":
      return { ...state, ...data };

    case "session/GET":
      return { ...state, ...data };

    case "session/GET_CSRF":
      return { ...state, ...data };

    case "session/DELETE":
      return model;

    default:
      return state;
  }
};
