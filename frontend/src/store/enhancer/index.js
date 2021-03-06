/* eslint-disable no-undef */

import { applyMiddleware, compose } from "redux";
import { createLogger } from "redux-logger";
import thunk from "redux-thunk";

let enhancer;

if (process.env.NODE_ENV === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = createLogger({
    collapsed: true,
  });
  const composeEnhancers =
    (window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ &&
      window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
        trace: true,
        traceLimit: 25,
      })) ||
    compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

export default enhancer;
