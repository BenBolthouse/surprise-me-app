/* eslint-disable no-undef */

import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";

import App from "./components/App.jsx";
import configureStore from "./store";

import * as actions from "./store/actions";

export const store = configureStore();

// Make Redux available on window only in development
if (process.env.NODE_ENV !== "production") {
  window.store = store;
  window.actions = actions;
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
