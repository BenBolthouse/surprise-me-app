import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import connections from "./reducers/connection.reducer";
import notifications from "./reducers/notification.reducer";
import user from "./reducers/user.reducer";

const rootReducer = combineReducers({
  connections,
  notifications,
  user,
});

const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
