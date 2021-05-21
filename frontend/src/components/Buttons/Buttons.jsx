/* eslint-disable react/prop-types */

import React from "react";
import { Link } from "react-router-dom";

import "./buttons.css";

const Button = (props) => {
  const {
    children,
    icon,
    onClick,
    disabled,
    importance,
    type,
    to,
  } = props;

  const classList = () => {
    let output = "button " + type + " ";

    output += importance ? importance + " " : "gray ";
    output += icon ? "has-icon" : "no-icon";

    return output;
  };

  const button = (
    <button
      disabled={disabled}
      onClick={onClick}>
      {!icon ? null : <div className="icon">{icon}</div>}
      {children}
    </button>
  );

  return (
    <div className={classList()}>
      {!to ?
        button :
        <Link to={to} tabIndex={-1}>
          {button}
        </Link>
      }
    </div>
  );
};

export const ButtonFill = (props) => {
  const _props = { ...props, type: "button-fill" };

  return <Button {..._props}>
    {props.children}
  </Button>
};

export const ButtonOutline = (props) => {
  const _props = { ...props, type: "button-outline" };

  return <Button {..._props}>
    {props.children}
  </Button>
};

export const ButtonText = (props) => {
  const _props = { ...props, type: "button-text" };

  return <Button {..._props}>
    {props.children}
  </Button>
};
