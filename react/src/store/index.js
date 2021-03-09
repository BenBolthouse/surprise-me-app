import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import security from './reducers/security';
import session from './reducers/session';

const rootReducer = combineReducers({
  security,
  session,
});

// Store config for export
const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
