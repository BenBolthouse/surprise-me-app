import { applyMiddleware, compose } from "redux";
import { createLogger } from "redux-logger"
import thunk from "redux-thunk";

let enhancer;

// Configure Chrome dev tools as enhancer
if (process.env.NODE_ENV === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = createLogger({
    collapsed: true,
  });
  logger.collapsed = true;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

export default enhancer;
