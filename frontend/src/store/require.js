import { store } from "../index";

/**
 * Determines if a session has been established by reading the Redux state
 * for a session id. Returns the session object or throws an error if not
 * found.
 */
export function requireSession() {
  const session = store.getState().session;

  if (!session.id) {
    throw new Error("A session is required to utilize this reducer.");
  }
  
  return session;
}

/**
 * Determines if a the csrf token is present. Returns true or throws an
 * error if not found.
 */
export function requireCsrf() {
  const token = store.getState().session.csrfToken;

  if (!token) {
    throw new Error("A csrf token is required to send this request.");
  }
  
  return true;
}
