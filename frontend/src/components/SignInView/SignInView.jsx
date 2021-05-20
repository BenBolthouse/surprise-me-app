/* eslint-disable react/no-unescaped-entities */
/* eslint-disable react/prop-types */

import { useDispatch } from "react-redux";
import { validate } from "validate.js"
import React, { useEffect, useRef, useState } from "react";
import {
  IoLockOpenOutline as Lock,
  IoMailOpenOutline as Email,
  IoCloseCircleOutline as Close,
} from "react-icons/io5"
import Loader from "react-loaders";
import 'loaders.css/src/animations/square-spin.scss'

import * as actions from "../../store/actions";
import TextInput from "../Inputs/TextInputs";

import "./sign_in_view.css";
import { ButtonFill, ButtonOutline } from "../Buttons/Buttons";

const SignInView = () => {
  const dispatch = useDispatch();
  const formRef = useRef(null);

  const [fetching, setFetching] = useState(false);
  const [allowTry, setAllowTry] = useState(false);
  const [email, setEmail] = useState({ value: "", errors: [], showErrors: false });
  const [password, setPassword] = useState({ value: "" });

  const emailOnChange = (evt) => {
    setEmail({ ...email, value: evt.target.value });
  }

  const emailOnBlur = () => {
    const constraints = {
      email: {
        presence: {
          allowEmpty: false,
          message: "is required.",
        },
        format: {
          pattern: /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/,
          message: "must be a valid email address.",
        },
      }
    }

    const result = validate({ email: email.value }, constraints);

    setEmail({ ...email, errors: result ? result.email : [] });
  }

  const emailOnErrorClick = () => {
    setEmail({ ...email, showErrors: !email.showErrors });
  }

  const passwordOnChange = (evt) => {
    setPassword({ value: evt.target.value });
  }

  const formOnSubmit = async (evt) => {
    evt.preventDefault();

    setFetching(true);

    await dispatch(actions.session.post({
      email: email.value,
      password: password.value,
    }));

    setFetching(false);
  };

  useEffect(() => {
    const readyToTry = !fetching
      && !email.errors.length
      && email.value.length
      && password.value.length;

    setAllowTry(!readyToTry);
  }, [fetching, email.errors, email.value, password.value])

  return (
    <div className="view sign-in-view">
      {!email.showErrors ? null :
        <div className="view errors-overlay">
          <div className="center">
            <Close className="close" onClick={emailOnErrorClick} />
            <h2>Please correct the following:</h2>
            <ul>
              {email.errors.map((error, i) => (
                <li key={"sign-in_email-error-" + i}>
                  <span className="check">✅</span>
                  {error}
                </li>
              ))}
            </ul>
          </div>
        </div>
      }
      {!fetching ? null :
        <div className="view fetching">
          <Loader type="square-spin" />
        </div>
      }
      <div className="center">
        <h1>Sign In</h1>
        <form ref={formRef} onSubmit={formOnSubmit}>
          <TextInput
            icon={<Email />}
            onChange={emailOnChange}
            onBlur={emailOnBlur}
            onErrorClick={emailOnErrorClick}
            errors={email.errors}
            name="email"
            formName="sign-in"
            label="Email" />
          <TextInput
            icon={<Lock />}
            onChange={passwordOnChange}
            errors={[]}
            name="password"
            formName="sign-in"
            label="Password"
            obscure={true} />
          <ButtonFill
            onClick={formOnSubmit}
            disabled={allowTry}
            importance="info">
            Sign in
          </ButtonFill>
        </form>
        <ButtonOutline to="/sign-up">
          Create an account
        </ButtonOutline>
      </div>
    </div>
  );
};

export default SignInView;
