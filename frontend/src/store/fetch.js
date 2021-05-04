/**
 * Base fetch API customized for connection to the service API.
 * 
 * @param {String} url URL for the request
 * @param {object} options Config object for fetch API function
 */
export const fetch = async (url, options = {}) => {
  const notGetRequest = options.method.toUpperCase() !== "GET";
  options.method = options.method || "GET";
  options.headers = options.headers || {};

  if (notGetRequest) {
    options.headers["Content-Type"] = "application/json";
    options.headers["X-CSRFToken"] = "";
  }

  const res = await window.fetch(url, options);
  const { message, data } = await res.json();

  if (res.status >= 400) throw res;

  return { message, data };
};
