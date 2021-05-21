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
  switch (type) {
    case "user/POST_EMAIL_UNIQUE":
      return { ...state, ...payload };

    case "user/POST":
      return { ...state, ...payload };

    case "user/GET":
      return { ...state, ...payload };

    case "user/PATCH":
      return { ...state, ...payload };

    case "user/PATCH_EMAIL":
      return { ...state, ...payload };

    case "user/PATCH_PASSWORD":
      return { ...state, ...payload };

    case "user/DELETE":
      return model;

    default:
      return state;
  }
};

export default reducer;
