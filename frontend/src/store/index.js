import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import Require from "./utilities/require"
import Socket from "./utilities/socket"

export const requires = new Require();
export const socket = new Socket();

import connections from "./reducers/connections";
import messages from "./reducers/messages";
import session from "./reducers/session";

const rootReducer = combineReducers({
  session,
  connections,
  messages,
});

const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
