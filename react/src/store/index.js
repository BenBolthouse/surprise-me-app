import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import connections from './reducers/connections';
import modal from './reducers/modal';
import notifications from './reducers/notifications';
import security from './reducers/security';
import session from './reducers/session';

const rootReducer = combineReducers({
  connections,
  modal,
  notifications,
  security,
  session,
});

// Store config for export
const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
