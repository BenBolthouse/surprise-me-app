import { store } from "../../src";

export const fetch = async (url, options = {}) => {
  // Get the Redux state
  const state = store.getState()

  options.method = options.method || "GET";
  options.headers = options.headers || {};

  if (options.method.toUpperCase() !== "GET") {
    options.headers["Content-Type"] =
      options.headers["Content-Type"] || "application/json";
    options.headers["X-CSRFToken"] = state.security.xCsrfToken;
  }

  const res = await window.fetch(url, options);
  const contentType = res.headers.get("content-type");

  if (contentType && contentType.includes("application/json")) {
    const data = await res.json();
    res.data = data;
  }

  if (res.status >= 400) throw res;

  return res;
};
