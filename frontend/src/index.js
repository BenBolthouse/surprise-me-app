/* eslint-disable no-undef */

import ErrorHandler from "./services/ErrorHandler";
import Fetch from "./services/Fetch";
import Socket from "./services/Socket";

export const handler = new ErrorHandler().handler;
export const api = new Fetch();
export const socket = new Socket();

import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";

import App from "./App.jsx";
import configureStore from "./store";

import * as connectionsActions from "./store/reducers/connections";
import * as messagesActions from "./store/reducers/messages";
import * as sessionActions from "./store/reducers/session";
import * as uiNotificationActions from "./store/reducers/ui-notifications";

export const store = configureStore();

// Make Redux available on window only in development
if (process.env.NODE_ENV !== "production") {
  window.store = store;
  window.connectionsActions = connectionsActions;
  window.messagesActions = messagesActions;
  window.sessionActions = sessionActions;
  window.uiNotificationActions = uiNotificationActions;
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
