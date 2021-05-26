/* eslint-disable react/prop-types */

import React, { useEffect, useRef, useState } from "react";
import {
  IoEyeOffOutline as EyeOff,
  IoEyeOutline as Eye,
  IoAlertCircleOutline as Errors,
  IoHelpCircleOutline as Help,
} from "react-icons/io5";

import "./index.css";

const TextInput = ({
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
  type,
  tried: _tried,
}) => {

  // eslint-disable-next-line no-undef
  const production = process.env.NODE_ENV === "production";

  const inputRef = useRef(null);

  const [focused, setFocused] = useState(false);
  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);

  const events = {
    inputOnChange: (evt) => {
      onChange && onChange(evt);
    },
    inputOnFocus: (evt) => {
      setFocused(true);
      onFocus && onFocus(evt);
    },
    inputOnBlur: (evt) => {
      setTried(true);
      onBlur && onBlur(evt);
    },
    viewPasswordOnClick: () => {
      setPasswordVisible(!passwordVisible);
    },
  };

  useEffect(() => {
    if (inputRef.current.value.length) setTrying(true);
    else setTrying(false);
  }, [inputRef, tried]);

  useEffect(() => {
    if (_tried) setTried(true);
  }, [_tried]);

  const inputClassList = () => {
    let _type = type === "password" ? "text-password" : type;

    let output = "user-input " + _type + " ";

    output += fetching ? "fetching " : "not-fetching ";
    output += focused ? "focused " : "not-focused ";
    output += trying ? "trying " : "not-trying ";
    output += tried ? "tried " : "not-tried ";
    output += errors && errors.length ? "errors " : "no-errors ";
    output += icon ? "has-icon" : "no-icon";

    return output;
  };

  return (
    <div className={inputClassList()}>
      {!icon ? null : <div className="icon-visual">{icon}</div>}
      <label htmlFor={`text-input_${formName}-${name}`}>{label}</label>
      <input
        ref={inputRef}
        onChange={events.inputOnChange}
        onFocus={events.inputOnFocus}
        onBlur={events.inputOnBlur}
        name={name}
        id={`text-input_${formName}-${name}`}
        disabled={disabled}
        autoComplete={production ? "on" : "chrome-off"}
        autoFocus={autoFocus || false}
        type={passwordVisible ? "text" : type}
      />
      <div className="icon-eye">
        {passwordVisible ? (
          <EyeOff onClick={events.viewPasswordOnClick} />
        ) : (
            <Eye onClick={events.viewPasswordOnClick} />
          )}
      </div>
      <div className="icon-errors">
        <Errors onClick={onErrorClick || null} />
      </div>
      <div className="icon-help">
        <Help onClick={null} />
      </div>
    </div>
  );
};

const FileInput = ({
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
  tried: _tried,
}) => {
  // eslint-disable-next-line no-undef
  const production = process.env.NODE_ENV === "production";

  const inputRef = useRef(null);

  const [focused, setFocused] = useState(false);
  const [trying, setTrying] = useState(false);
  const [tried, setTried] = useState(false);

  const events = {
    inputOnChange: (e) => {
      const mimetype = e.target.files[0].type.includes("image/");

      if (!mimetype) return;

      onChange && onChange(e);
    },
    aliasOnFocus: (e) => {
      setFocused(true);
      onFocus && onFocus(e);
    },
    aliasOnBlur: (e) => {
      setTried(true);
      onBlur && onBlur(e);
    },
    aliasOnClick: (e) => {
      e.preventDefault();
      inputRef.current.click();
    }
  };

  useEffect(() => {
    if (inputRef.current.value.length) setTrying(true);
    else setTrying(false);
  }, [inputRef, tried]);

  useEffect(() => {
    if (_tried) setTried(true);
  }, [_tried]);

  const inputClassList = () => {
    let output = "user-input file ";

    output += fetching ? "fetching " : "not-fetching ";
    output += focused ? "focused " : "not-focused ";
    output += trying ? "trying " : "not-trying ";
    output += tried ? "tried " : "not-tried ";
    output += errors && errors.length ? "errors " : "no-errors ";
    output += icon ? "has-icon" : "no-icon";

    return output;
  };

  return (
    <div className={inputClassList()}>
      <div className="preview">
        {!icon ? null : <div className="icon-visual">{icon}</div>}
      </div>
      <input
        accept="image/*"
        ref={inputRef}
        onChange={events.inputOnChange}
        name={name}
        id={`file-input_${formName}-${name}`}
        disabled={disabled}
        autoComplete={production ? "on" : "chrome-off"}
        autoFocus={autoFocus || false}
        type={"file"}
      />
      <button
        onClick={events.aliasOnClick}
        onFocus={events.aliasOnFocus}
        onBlur={events.aliasOnBlur}>
        {label}
      </button>
      <div className="icon-errors">
        <Errors onClick={onErrorClick || null} />
      </div>
    </div>
  );
}

export const TextInput = (props) => {
  const _props = { ...props, type: "text" };

  return <TextInput {..._props} />;
};

export const EmailInput = (props) => {
  const _props = { ...props, type: "email" };

  return <TextInput {..._props} />;
};

export const PasswordInput = (props) => {
  const _props = { ...props, type: "password" };

  return <TextInput {..._props} />;
};

export const ImageInput = (props) => {
  const _props = { ...props, type: "image" };

  return <File {..._props} />;
};
