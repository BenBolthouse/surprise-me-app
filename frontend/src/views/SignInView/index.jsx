/* eslint-disable react/prop-types */

import { useRouteMatch } from "react-router-dom";
import { useDispatch } from "react-redux";
import React, { useEffect, useState } from "react";

import {
  IoAlertCircleSharp as Errors,
  IoCloseCircleSharp as Close,
  IoEyeOutline as ShowPassword,
  IoEyeOffOutline as HidePassword,
} from "react-icons/io5"

import {
  EmailInput,
  PasswordInput,
} from "../../components";

import { actions } from "../../store";

import { validationConstraints } from "../../utilities";

import "./styles.css";

export function SignInView() {
  const dispatch = useDispatch();

  const pathMatch = useRouteMatch({
    path: "/start/sign-in",
    exact: true,
  });

  const [email, setEmail] = useState({
    value: "",
    errors: [],
    showErrors: false,
    tried: false,
  });

  const [password, setPassword] = useState({
    value: "",
    errors: [],
    showErrors: false,
    tried: false,
  });

  const [showErrors, setShowErrors] = useState(false);

  const [canSubmit, setCanSubmit] = useState(false);

  const [submitting, setSubmitting] = useState(false);

  async function handleFormOnSubmit(e) {
    e.preventDefault();

    setSubmitting(true);

    await dispatch(actions.session.post({
      email: email.value,
      password: password.value
    }));

    setSubmitting(false);
  }

  const viewComponent = {
    className: "view sign-in-view",
    "view-path-match": pathMatch ? "match" : "no-match",
  }

  const centerElement = {
    className: "view-content center",
  }

  const formElement = {
    onSubmit: handleFormOnSubmit,
    "br-awaiting": submitting.toString(),
  }

  const showErrorsElement = {
    className: "view-dim " + (showErrors ? "show" : "hide"),
  }

  const emailInputProps = {
    name: "email",
    state: email,
    setState: setEmail,
    validationAttributes: { email: email.value },
    validationConstraints: {
      email: {
        ...validationConstraints.required,
        ...validationConstraints.email,
      }
    },
    icons: {
      showErrors: <Errors />,
      hideErrors: <Close />,
    },
    tryOn: "onblur",
  }

  const submitButtonElement = {
    disabled: !canSubmit,
  }

  const passwordInputProps = {
    name: "password",
    state: password,
    setState: setPassword,
    validationAttributes: { password: password.value },
    validationConstraints: { password: validationConstraints.required },
    icons: {
      showErrors: <Errors />,
      hideErrors: <Close />,
      showPassword: <ShowPassword />,
      hidePassword: <HidePassword />,
    },
    tryOn: "onblur",
  }

  // Side effect disables the form submit button if errors are present or
  // values are empty.
  useEffect(() => {
    const _canSubmit = (
      email.value.length && !email.errors.length &&
      password.value.length && !password.errors.length);

    setCanSubmit(_canSubmit);
  }, [email.value, password.value])

  // Side effect detects changes in showErrors values for inputs and sets
  // the showErrors state accordingly.
  useEffect(() => {
    const _showErrors = (email.showErrors || password.showErrors);

    setShowErrors(_showErrors);
  }, [email.showErrors, password.showErrors])

  return (
    <div {...viewComponent}>
      <div {...showErrorsElement} />
      <div {...centerElement}>
        <h1>Sign in</h1>
        <form {...formElement}>
          <EmailInput {...emailInputProps} />
          <PasswordInput {...passwordInputProps} />
          <button {...submitButtonElement}>Go</button>
        </form>
      </div>
    </div>
  );
}
