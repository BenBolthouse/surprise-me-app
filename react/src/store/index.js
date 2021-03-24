import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import chat from './reducers/chat';
import connections from './reducers/connections';
import localStorage from './reducers/localStorage';
import modal from './reducers/modal';
import security from './reducers/security';
import session from './reducers/session';

const rootReducer = combineReducers({
  chat,
  connections,
  localStorage,
  modal,
  security,
  session,
});

// Store config for export
const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
