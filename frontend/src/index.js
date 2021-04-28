import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";

import App from "./App.jsx";
import configureStore from "./store";

import * as chatActions from "./store/reducers/chat";
import * as connectionsActions from "./store/reducers/connections";
import * as localStorageActions from "./store/reducers/localStorage";
import * as sessionActions from "./store/reducers/session";

export const store = configureStore();

// Make Redux available on window only in development
if (process.env.NODE_ENV !== 'production') {
  window.store = store;
  window.chatActions = chatActions;
  window.connectionsActions = connectionsActions;
  window.localStorageActions = localStorageActions;
  window.sessionActions = sessionActions;
}

// React root entry point
ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);
