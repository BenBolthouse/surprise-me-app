import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import connections from "./reducers/connections.reducer";
import notifications from "./reducers/notifications.reducer";
import session from "./reducers/session.reducer";
import user from "./reducers/user.reducer";

const rootReducer = combineReducers({
  connections,
  notifications,
  session,
  user,
});

const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
