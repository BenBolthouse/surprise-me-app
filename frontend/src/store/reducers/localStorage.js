// State template
const localStorageTemplate = {
  timestamp: null,
  chat: {},
};

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = localStorageTemplate, { type, payload }) => {
  switch (type) {
    // ********************
    default:
      return state;
  }
};

export default reducer;
