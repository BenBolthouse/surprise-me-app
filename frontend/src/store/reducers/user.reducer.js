const model = {
  id: null,
  firstName: null,
  lastName: null,
  email: null,
  bio: null,
  latitude: null,
  longitude: null,
  createdAt: null,
  updatedAt: null,
  type: null,
};

const reducer = (state = model, { type, payload }) => {
  const data = payload ? payload.data : null;

  switch (type) {
    case "user/POST_EMAIL_UNIQUE":
      return { ...state, ...data };

    case "user/POST":
      return { ...state, ...data };

    case "user/GET":
      return { ...state, ...data };

    case "user/PATCH":
      return { ...state, ...data };

    case "user/PATCH_EMAIL":
      return { ...state, ...data };

    case "user/PATCH_PASSWORD":
      return { ...state, ...data };

    case "user/DELETE":
      return model;

    default:
      return state;
  }
};

export default reducer;
