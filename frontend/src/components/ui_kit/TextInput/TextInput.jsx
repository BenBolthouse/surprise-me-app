/* eslint-disable react/prop-types */

import React, { useEffect, useState } from "react";
import { IoAlertCircle as Alert } from "react-icons/io5"
import { IoHelpCircle as Help } from "react-icons/io5"

import "./text_input.css"

const TextInput = ({
  id,
  name,
  onBlur,
  onChange,
  onError,
  onFocus,
  onHelp,
  helpText,
  errors,
  placeholder = "",
}) => {

  const [_value, _setValue] = useState("");
  const [_errors, _setHasErrors] = useState(false);
  const [_focused, _setIsFocused] = useState(false);
  const [_tried, _setHasTried] = useState(false);
  const [_trying, _setIsTrying] = useState(false);

  useEffect(() => {
    if (_value.length) _setIsTrying(true);
    else if (!_value.length) _setIsTrying(false);
  }, [_value]);

  useEffect(() => {
    if (_trying && !_focused) _setHasTried(true);
  }, [_trying, _focused]);

  useEffect(() => {
    if (_tried && errors.length) _setHasErrors(true);
  }, [errors])

  const _onChange = (evt) => {
    onChange && onChange(evt);
    _setValue(evt.target.value);
  };

  const _onFocus = (evt) => {
    onFocus && onFocus(evt);
    _setIsFocused(true);
  };

  const _onBlur = (evt) => {
    onBlur && onBlur(evt);
    _setIsFocused(false);
  };

  const classErrors = _errors ? " invalid" : " valid";
  const classFocused = _focused ? " focused" : " unfocused";
  const classTried = _tried ? " tried" : " not-tried";
  const classTrying = _trying ? " trying" : " not-trying";

  return (
    <div className={"text-input" +
      classFocused +
      classErrors +
      classTried +
      classTrying}>
      <div className="input-group">
        <label
          htmlFor={"text-input-" + id}>
          {name}
        </label>
        <input
          id={"text-input-" + id}
          type="text"
          value={_value}
          placeholder={placeholder}
          onChange={e => _onChange(e)}
          onFocus={e => _onFocus(e)}
          onBlur={e => _onBlur(e)} />
        <div className="controls">
          <Alert onClick={() => onError && onError(errors)} />
          <Help onClick={() => onHelp && onHelp(helpText)} />
        </div>
      </div>
      <div className="errors">
        <ul>
          {errors.map((err, i) => (
            <li key={"input-error-" + i}>{err}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default TextInput;
