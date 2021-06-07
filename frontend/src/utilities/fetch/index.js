import { store } from "../..";

import camelcase from "camelcase-keys";
import snakecase from "snakecase-keys";

import { actions } from "../../store";

export async function get(url) {
  return await this.fetch(url, { method: "GET" });
}

export async function post(url, body) {
  return await this.fetch(url, { method: "POST", body });
}

export async function put(url, body) {
  return await this.fetch(url, { method: "PUT", body });
}

export async function patch(url, body) {
  return await this.fetch(url, { method: "PATCH", body });
}

export async function destroy(url) {
  return await this.fetch(url, { method: "DELETE" });
}

export async function fetch(url, options = {}) {
  const csrf = store.getState().session.csrfToken;

  const defaultOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  };

  const request = { ...defaultOptions, ...options };

  const stateChangeReq = "POST PUT PATCH DELETE".includes(request.method);

  if (stateChangeReq) {
    if (request.body) {
      const convertCase = snakecase(request.body, { deep: true });
      request.body = JSON.stringify(convertCase);
    }
    request.headers["X-CSRFToken"] = csrf;
  }

  let response = await window.fetch(url, request);

  const { status } = response;

  response = await response.json();
  response = camelcase(response, { deep: true });

  const { notification, data } = response;

  if (notification)
    switch (notification.type) {
      case "popup":
        store.dispatch(actions.notifications.popup.create(notification));
        break;
      case "card":
        store.dispatch(actions.notifications.card.create(notification));
        break;
    }

  if (stateChangeReq) store.dispatch(actions.session.getCsrf());

  return { data, status };
}
