/* eslint-disable react/prop-types */

import React, { useEffect, useState } from "react";
import {
  IoAlertCircleOutline as Errors,
  IoHelpCircleOutline as Help
} from "react-icons/io5"

import "./text_inputs.css";

const TextInput = (props) => {
  const {
    icon,
    onChange,
    onFocus,
    onBlur,
    onHelpClick,
    onErrorClick,
    errors,
    name,
    formName,
    label,
    obscure,
  } = props;

  const [value, setValue] = useState("");
  const [focused, setFocused] = useState(false);
  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);

  const inputOnChange = (evt) => {
    setValue(evt.target.value);
    onChange && onChange(evt);
  }

  const inputOnFocus = (evt) => {
    setFocused(true)
    onFocus && onFocus(evt);
  }

  const inputOnBlur = (evt) => {
    setTried(true)
    onBlur && onBlur(evt);
  }

  useEffect(() => {
    if (value.length) {
      setTrying(true)
    }
    else {
      setTrying(false)
    }
  }, [value.length, tried])

  const inputClassList = () => {
    let output = "text-input ";

    output += focused ? "focused " : "not-focused ";
    output += trying ? "trying " : "not-trying ";
    output += tried ? "tried " : "not-tried ";
    output += errors.length ? "errors " : "no-errors ";
    output += icon ? "has-icon" : "no-icon";

    return output;
  }

  const inputType = obscure ? "password" : "text";

  return (
    <div className={inputClassList()}>
      {!icon ? null : <div className="icon">{icon}</div>}
      <label htmlFor={`text-input_${formName}-${name}`}>{label}</label>
      <input type={inputType}
        name={name} id={`text-input_${formName}-${name}`}
        onChange={inputOnChange}
        onFocus={inputOnFocus}
        onBlur={inputOnBlur}
        value={value} />
      <Errors className="icon-errors" onClick={onErrorClick || null} />
      <Help className="icon-help" onClick={onHelpClick || null} />
    </div>
  )
}

export default TextInput;
