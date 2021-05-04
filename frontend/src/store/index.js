import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import connections from "./reducers/connections";
import session from "./reducers/session";

const rootReducer = combineReducers({
  connections,
  session,
});

const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
