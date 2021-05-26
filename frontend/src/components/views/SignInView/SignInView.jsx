/* eslint-disable react/no-unescaped-entities */
/* eslint-disable react/prop-types */

import { useDispatch } from "react-redux";
import Loader from "react-loaders";
import React, { useEffect, useState } from "react";

import {
  IoLockOpenOutline as Lock,
  IoMailOpenOutline as Email,
  IoCloseCircleOutline as Close,
} from "react-icons/io5";

import { ButtonFill, ButtonOutline } from "../../Buttons";
import { PasswordInput, TextInput } from "../../Inputs";
import * as actions from "../../../store/actions";
import * as validate from "../../_validation";

import "loaders.css/src/animations/square-spin.scss";
import "./sign_in_view.css";

// prettier-ignore
const emailPattern = /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/;

const SignInView = () => {
  const dispatch = useDispatch();

  const [email, setEmail] = useState({
    value: "",
    errors: [],
  });
  const [password, setPassword] = useState({
    value: "",
    errors: [],
  });
  const [passwordInvalid, setPasswordInvalid] = useState(false);
  const [errors, setErrors] = useState([]);
  const [errorsVisible, setErrorsVisible] = useState(false);
  const [formFetching, setFormFetching] = useState(false);
  const [submitDisable, setSubmitDisable] = useState(true);

  // ——— validation ———————————————————————————————————————————————————————————
  const validation = {
    email: () => {
      const errors = validate.email(email.value);
      setEmail({ ...email, errors });

      return errors.length === 0;
    },
  };

  // ——— events ———————————————————————————————————————————————————————————————
  const events = {
    errorsOpenOnClick: () => setErrorsVisible(true),
    errorsCloseOnClick: () => setErrorsVisible(false),
    emailOnChange: (e) => {
      setEmail({ ...email, value: e.target.value });
    },
    passwordOnChange: (e) => {
      setPassword({ ...password, value: e.target.value, errors: [] });
      setPasswordInvalid(false);
    },
    formOnSubmit: async (e) => {
      e.preventDefault();

      setFormFetching(true);

      const { payload } = await dispatch(
        actions.session.post({
          email: email.value,
          password: password.value,
        })
      );

      const { status } = payload;

      if (status === 400) {
        setPasswordInvalid(true);
        setPassword({ ...password, errors: ["Invalid password."] });
      }

      setFormFetching(false);
    },
  };

  // ——— side effects —————————————————————————————————————————————————————————

  // Side effect runs validation on all fields when a change in input value
  // is discovered.
  useEffect(() => {
    validation.email();
  }, [email.value]);

  // Side effect populates the error array when a change in input error
  // value is discovered.
  useEffect(() => {
    const errors = [
      ...email.errors,
      ...(passwordInvalid ? ["Password must be valid."] : []),
    ];

    setErrors(errors);
  }, [email.errors, passwordInvalid]);

  // Side effect handles disabling the "next" button if fields are empty or
  // errors are present.
  useEffect(() => {
    const x = !(
      email.value.match(emailPattern) &&
      !email.errors.length &&
      !formFetching
    );

    setSubmitDisable(x);
  }, [email.value, email.errors]);

  // ——— DOM classes ——————————————————————————————————————————————————————————
  const classList = {
    errors: "view errors " + (errorsVisible ? "show" : "hide"),
    formFetching: "view fetching " + (formFetching ? "show" : "hide"),
  };

  // ——— render ———————————————————————————————————————————————————————————————
  return (
    <div className="view sign-in-view">
      <div className={classList.errors} onClick={events.errorsCloseOnClick}>
        <div className="center">
          <div className="close">
            <Close />
          </div>
          <h2>Please correct the following:</h2>
          <ul>
            {errors.map((error, i) => (
              <li key={"sign-in-form-error-" + i}>
                <div className="check">✅</div>
                {error}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className={classList.formFetching}>
        <Loader type="square-spin" />
      </div>
      <div className="center">
        <h1>Sign In</h1>
        <form>
          <TextInput
            icon={<Email />}
            autoFocus={true}
            errors={email.errors}
            formName="sign-in"
            label="Email"
            name="email"
            onChange={events.emailOnChange}
            onErrorClick={events.errorsOpenOnClick}
          />
          <PasswordInput
            icon={<Lock />}
            errors={password.errors}
            formName="sign-in"
            label="Password"
            name="password"
            onChange={events.passwordOnChange}
            onErrorClick={events.errorsOpenOnClick}
          />
          <ButtonFill
            onClick={events.formOnSubmit}
            disabled={submitDisable}
            importance="info"
          >
            Sign in
          </ButtonFill>
        </form>
        <ButtonOutline to="/sign-up" importance="info">
          Create an account
        </ButtonOutline>
      </div>
    </div>
  );
};

export default SignInView;
