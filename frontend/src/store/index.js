import { createStore, combineReducers } from "redux";

import enhancer from "./enhancer";

import connections from "./reducers/connections";
import messages from "./reducers/messages";
import products from "./reducers/products";
import session from "./reducers/session";
import sessionNotifications from "./reducers/session-notifications";
import uiNotifications from "./reducers/ui-notifications";

const rootReducer = combineReducers({
  session,
  connections,
  messages,
  products,
  sessionNotifications,
  uiNotifications,
});

const configureStore = (preloadedState) =>
  createStore(rootReducer, preloadedState, enhancer);

export default configureStore;
