/* eslint-disable react/prop-types */

import React, { useEffect, useState } from "react";

import {
  IoAlertCircleSharp as Errors,
  IoCloseCircleSharp as Close,
  IoEyeSharp as ShowPassword,
  IoEyeOffSharp as HidePassword,
} from "react-icons/io5"

import {
  EmailInput,
  PasswordInput,
  View,
  ViewRouteMatchHandler,
} from "../../components";

import { validationConstraints } from "../../utilities";

export function SignInView() {
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

  function handleFormOnSubmit(e) {
    e.preventDefault();
  }

  const centerElement = {
    className: "view-content center",
  }

  const formElement = {
    onSubmit: handleFormOnSubmit,
  }

  const showErrorsElement = {
    className: "view-dim " + (showErrors ? "show" : "hide"),
  }

  const emailInputProps = {
    name: "email",
    state: email,
    setState: setEmail,
    validationAttributes: { email: email.value },
    validationConstraints: { email: validationConstraints.required },
    icons: {
      showErrors: <Errors />,
      hideErrors: <Close />,
    },
    tryOn: "onblur",
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

  const submitButtonElement = {
    disabled: !canSubmit,
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
    <ViewRouteMatchHandler exact path="/start/sign-in">
      <View name="sign-in">
        <div {...showErrorsElement} />
        <div {...centerElement}>
          <h1>Sign in</h1>
          <form {...formElement}>
            <EmailInput {...emailInputProps} />
            <PasswordInput {...passwordInputProps} />
            <button {...submitButtonElement}>Go</button>
          </form>
        </div>
      </View>
    </ViewRouteMatchHandler>
  );
}
