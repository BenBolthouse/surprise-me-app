// State template
const modalTemplate = {
  component: [],
  clearOnClick: null,
  onClearCallback : null,
}

// ** «««««««««««««««««««««««« Actions »»»»»»»»»»»»»»»»»»»»»»»» **

const SET_MODAL = "modal/setModal";

export const setModal = (modalObject) => ({
  type: SET_MODAL,
  payload: modalObject,
});

const CLEAR_MODAL = "modal/clearModal";

export const clearModal = () => ({
  type: CLEAR_MODAL,
});

// ** «««««««««««««««««««««««« Reducer »»»»»»»»»»»»»»»»»»»»»»»» **

const reducer = (state = modalTemplate, { type, payload }) => {

  switch (type) {

    case SET_MODAL:
      return {
        component: [payload.component],
        clearOnClick: payload.clearOnClick,
        onClearCallback: payload.onClearCallback,
      }

    case CLEAR_MODAL:
      return { ...modalTemplate }

    default:
      return state;

  }
}

export default reducer;
