/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";

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
  });

  const [password, setPassword] = useState({
    value: "",
    errors: [],
  });

  const [canSubmit, setCanSubmit] = useState(false);

  function handleFormOnSubmit(e) {
    e.preventDefault();
  }

  function handleEmailOnChange(e) {
    setEmail({ ...email, value: e.target.value });
  }

  function handleEmailOnBlur(e) {
    e.preventDefault();
  }

  function handlePasswordOnChange(e) {
    setPassword({ ...password, value: e.target.value });
  }

  function handlePasswordOnBlur(e) {
    e.preventDefault();
  }

  const centerElement = {
    className: "center",
  }

  const formElement = {
    onSubmit: handleFormOnSubmit,
  }

  const emailInputElement = {
    onChange: handleEmailOnChange,
    onBlur: handleEmailOnBlur,
    value: email.value,
  }

  const passwordInputElement = {
    onChange: handlePasswordOnChange,
    onBlur: handlePasswordOnBlur,
    value: password.value,
  }

  const emailInputProps = {
    name: "email",
    element: emailInputElement,
    state: email,
    setState: setEmail,
    validationAttributes: { email: email.value },
    validationConstraints: { email: validationConstraints.required },
  }

  const passwordInputProps = {
    name: "password",
    element: passwordInputElement,
    state: password,
    setState: setPassword,
    validationAttributes: { password: password.value },
    validationConstraints: { password: validationConstraints.required },
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

    if (_canSubmit) {
      setCanSubmit(true);
    } else {
      setCanSubmit(false);
    }
  }, [email, password])

  return (
    <ViewRouteMatchHandler exact path="/start/sign-in">
      <View name="sign-in">
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
