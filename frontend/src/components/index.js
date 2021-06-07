/** @module components */

import {
  SessionHandler as _SessionHandler,
  Authenticated as _Authenticated,
  Anonymous as _Anonymous,
} from "./SessionHandler";

import {
  EmailInput as _EmailInput,
  PasswordInput as _PasswordInput,
} from "./inputTextTypes";

import {
  View as _View,
  ViewRouteMatchHandler as _ViewRouteMatchHandler,
} from "./View";

/**
 * @function
 * @description
 * Component wraps the whole application and handles setup of the user
 * interface by requesting session-related data which is then dispatched to
 * Redux.
 */
export const SessionHandler = _SessionHandler;

/**
 * @function
 * @description
 * Component wraps views to provide an automatic redirect in the event that
 * a session doesn't exist.
 * @param {String} redirect
 * The path to redirect to if the user does not have an active session
 */
export const Authenticated = _Authenticated;

/**
 * @function
 * @description
 * Component wraps views to provide an automatic redirect in the event that
 * a session exists.
 * @param {String} redirect
 * The path to redirect to if the user has an active session
 */
export const Anonymous = _Anonymous;

/**
 * @function
 * @description
 * Component renders an email input with control over **validation
 * constraints**, **validation timing** based on event triggers, **input
 * event handlers and attributes**, and **conditional rendering of input
 * errors** based on user interaction. Component also **binds to an argued
 * state variable and update function** of a parent component whom is
 * utilizing `React.useState`.
 * @param {String} name
 * Name of the input; must match the name of the variable given for
 * `state`, e.g. if `state` is an implementation of `React.useState` as
 * such: `var [foobar, setFoobar] = useState({...})` then `name` must also
 * equal "foobar".
 * @param {object} element
 * Element props for the input element
 * @param {object} state
 * State object from React's `useState` hook
 * @param {Function} setState
 * State update function from React's `useState` hook
 * @param {object} validationAttributes
 * First argument of validation.js validate function
 * @param {object} validationConstraints
 * Second argument of validation.js validate function
 * @param {object} icons
 * Collection of React icon components: `{ showErrors,
 * hideErrors, showHelp, hideHelp, showPassword, hidePassword }`
 * @param {String} tryOn
 * Indicates the event which triggers the input to "try", i.e. display
 * validation results, if any. Available options are **onload**,
 * **onchange**, **onblur**, and **onfocus**. Defaults to **onchange**.
 */
export const EmailInput = _EmailInput;

/**
 * @function
 * @description
 * Component renders a password input with control over **validation
 * constraints**, **validation timing** based on event triggers, **input
 * event handlers and attributes**, and **conditional rendering of input
 * errors** based on user interaction. Component also **binds to an argued
 * state variable and update function** of a parent component whom is
 * utilizing `React.useState`.
 * @param {String} name
 * Name of the input; must match the name of the variable given for
 * `state`, e.g. if `state` is an implementation of `React.useState` as
 * such: `var [foobar, setFoobar] = useState({...})` then `name` must also
 * equal "foobar".
 * @param {object} element
 * Element props for the input element
 * @param {object} state
 * State object from React's `useState` hook
 * @param {Function} setState
 * State update function from React's `useState` hook
 * @param {object} validationAttributes
 * First argument of validation.js validate function
 * @param {object} validationConstraints
 * Second argument of validation.js validate function
 * @param {object} icons
 * Collection of React icon components: `{ showErrors,
 * hideErrors, showHelp, hideHelp, showPassword, hidePassword }`
 * @param {String} tryOn
 * Indicates the event which triggers the input to "try", i.e. display
 * validation results, if any. Available options are **onload**,
 * **onchange**, **onblur**, and **onfocus**. Defaults to **onchange**.
 */
export const PasswordInput = _PasswordInput;

/**
 * @function
 * @description
 * Component renders an application view.
 * @param {String} name
 * Name of the view; must be uniquely named in the application scope
 */
export const View = _View;

/**
 * @function
 * @description
 * Renders `components.View` with an additional HTML attribute
 * `br-view-match` whose value equals "match" or "no-match" based on URL
 * path matching.
 * @param {String} name
 * Name of the view; must be uniquely named in the application scope
 * @param {String} path
 * The URL path to match
 * @param {Boolean} exact
 * Same as the react-dom-router's Route component prop `exact`; will only
 * match if exactly the path provided
 */
export const ViewRouteMatchHandler = _ViewRouteMatchHandler;
