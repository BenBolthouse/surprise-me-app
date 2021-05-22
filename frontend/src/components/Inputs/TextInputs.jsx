/* eslint-disable no-undef */
/* eslint-disable react/prop-types */

import React, { useEffect, useRef, useState } from "react";
import {
  IoAlertCircleOutline as Errors,
  IoHelpCircleOutline as Help
} from "react-icons/io5"

import "./text_inputs.css";

const Input = (props) => {
  const {
    autoFocus,
    disabled,
    errors,
    fetching,
    formName,
    icon,
    label,
    name,
    onBlur,
    onChange,
    onErrorClick,
    onFocus,
    onHelpClick,
    tried: _tried,
  } = props;

  const production = process.env.NODE_ENV === "production";

  const inputRef = useRef(null);

  const [focused, setFocused] = useState(false);
  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);

  const inputOnChange = (evt) => {
    onChange(evt);
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
    if (inputRef.current.value.length) setTrying(true)
    else setTrying(false)
  }, [inputRef, tried])

  useEffect(() => {
    if (_tried) setTried(true)
  }, [_tried])

  const inputClassList = () => {
    let output = "text-input ";

    output += fetching ? "fetching " : "not-fetching ";
    output += focused ? "focused " : "not-focused ";
    output += trying ? "trying " : "not-trying ";
    output += tried ? "tried " : "not-tried ";
    output += errors && errors.length ? "errors " : "no-errors ";
    output += icon ? "has-icon" : "no-icon";

    return output;
  }

  return (
    <div className={inputClassList()}>
      {!icon ? null :
        <div className="icon">
          {icon}
        </div>
      }
      <label htmlFor={`text-input_${formName}-${name}`}>
        {label}
      </label>
      <input
        onChange={inputOnChange}
        onFocus={inputOnFocus}
        onBlur={inputOnBlur}
        ref={inputRef}
        name={name} id={`text-input_${formName}-${name}`}
        disabled={disabled}
        autoComplete={production ? "on" : "chrome-off"}
        autoFocus={autoFocus || false}
      />
      <Errors className="icon-errors" onClick={onErrorClick || null} />
      <Help className="icon-help" onClick={onHelpClick || null} />
    </div>
  )
}

export const TextInput = (props) => {
  const _props = {...props, inputType: "text"}

  return <Input {..._props} />
}

export const EmailInput = (props) => {
  const _props = {...props, inputType: "email"}

  return <Input {..._props} />
}

export const PasswordInput = (props) => {
  const _props = {...props, inputType: "password"}

  return <Input {..._props} />
}
