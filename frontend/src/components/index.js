/** @module components */

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
 * Component renders an email input with control over **validation
 * constraints**, **validation timing** based on event triggers, **input
 * event handlers and attributes**, and **conditional rendering of input
 * errors** based on user interaction. Component also **binds to an argued
 * state variable and update function** of a parent component whom is
 * utilizing `React.useState`.
 * @param {String} name
 * Name of the view; must be uniquely named in the application scope
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
 * Name of the input; must be uniquely named in the application scope
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
 */
export const PasswordInput = _PasswordInput;

/**
 * @function
 * @description
 * Component renders an application view.
 * @param {String} name
 * Name of the input; must be uniquely named in the application scope
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
 * match if exact
 */
export const ViewRouteMatchHandler = _ViewRouteMatchHandler;
