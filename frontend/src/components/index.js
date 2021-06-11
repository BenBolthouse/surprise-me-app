/** @module components */

import {
  EmailInput as _EmailInput,
  PasswordInput as _PasswordInput,
} from "./interface/inputTextTypes";

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
