/* eslint-disable react/prop-types */

import React, { useEffect, useState } from "react";
import { PasswordInput } from "../../Inputs";

import {
  IoLockOpenOutline as Lock,
} from "react-icons/io5";

import { ButtonFill, ButtonText } from "../../Buttons";
import * as validate from "../../_validations";


// Styles for individual frames imported on the parent component.

const PasswordFrame = ({
  framePosition,
  setFramePosition,
  state,
  setState,
  showErrors,
}) => {
  // ——— state ————————————————————————————————————————————————————————————————
  const [password, setPassword] = useState({
    value: "",
    errors: [],
  });
  const [confirmPassword, setConfirmPassword] = useState({
    value: "",
    errors: [],
  });
  const [errors, setErrors] = useState([]);
  const [formDisable, setFormDisable] = useState(false);
  const [nextDisable, setNextDisable] = useState(true);

  // ——— validation ———————————————————————————————————————————————————————————
  const validation = {
    password: () => {
      const errors = validate.password(password.value);
      setPassword({ ...password, errors });

      return errors.length === 0;
    },
    confirmPassword: () => {
      const errors = validate.confirmPassword(password.value, confirmPassword.value);
      setConfirmPassword({ ...confirmPassword, errors });

      return errors.length === 0;
    },
  };

  // ——— events ———————————————————————————————————————————————————————————————
  const events = {
    passwordOnChange: (e) => {
      setPassword({ ...password, value: e.target.value });
    },
    confirmPasswordOnChange: (e) => {
      setConfirmPassword({ ...confirmPassword, value: e.target.value });
    },
    formBackOnClick: () => {
      setFramePosition(framePosition - 1);
    },
    formOnSubmit: () => {
      const valid =
        validation.password() &&
        validation.confirmPassword();

      if (valid) {
        setFramePosition(framePosition + 1);
        setState({
          ...state,
          password: password.value,
        });
      } else {
        setNextDisable(true);
      }
    },
    errorIconOnClick: () => {
      showErrors(errors);
    },
  }

  // ——— side effects —————————————————————————————————————————————————————————

  // Side effect runs validation on all fields when a change in input value
  // is discovered.
  useEffect(() => {
    validation.password();
    validation.confirmPassword();
  }, [password.value, confirmPassword.value]);

  // Side effect populates the error array when a change in input error
  // value is discovered.
  useEffect(() => {
    const errors = [
      ...password.errors,
      ...confirmPassword.errors,
    ];

    setErrors(errors);
  }, [password.errors, confirmPassword.errors]);

  // Side effect handles disabling the "next" button if fields are empty or
  // errors are present.
  useEffect(() => {
    const x = !(
      password.value.length &&
      confirmPassword.value.length &&
      !password.errors.length &&
      !confirmPassword.errors.length &&
      framePosition === 1
    );

    setNextDisable(x);
  }, [
    password.value,
    password.errors,
    confirmPassword.value,
    confirmPassword.errors,
    framePosition,
  ]);

  // Side effect simply prevents additional changes to this frame's fields
  // once the user has advanced to another position.
  useEffect(() => {
    if (framePosition !== 1) setFormDisable(true);
    else if (framePosition === 1) setFormDisable(false);
  }, [framePosition]);

  return (
    <div className="frame frame-b">
      <h2>Choose a Password</h2>
      <form autoComplete="chrome-off">
        <PasswordInput
          icon={<Lock />}
          autoFocus={framePosition === 1}
          disabled={formDisable}
          errors={password.errors}
          formName="sign-up"
          label="Password"
          name="password"
          onChange={events.passwordOnChange}
          onErrorClick={events.errorIconOnClick}
        />
        <PasswordInput
          icon={<Lock />}
          disabled={formDisable}
          errors={confirmPassword.errors}
          formName="sign-up"
          label="Confirm"
          name="confirmPassword"
          onChange={events.confirmPasswordOnChange}
          onErrorClick={events.errorIconOnClick}
        />
      </form>
      <ButtonText
        onClick={events.formBackOnClick}
      >
        Back
      </ButtonText>
      <ButtonFill
        onClick={events.formOnSubmit}
        disabled={nextDisable}
        importance="info"
      >
        Next
      </ButtonFill>
      <span>Step 1 of 4</span>
    </div>
  );
}

export default PasswordFrame;
