import React from 'react';
import { BsExclamationSquare, BsX } from "react-icons/bs";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useState } from "react";
import Loader from "react-loading";

import { fetch } from "../../services/fetch";

import {
  checkboxValidation,
  emailValidation,
  nameValidation,
  passwordValidation,
  stateValidation,
} from "../../validation";

import * as sessionActions from "../../store/reducers/session";

const Signup = () => {
  // Hooks
  const dispatch = useDispatch();

  // Component state
  const [firstName, setFirstName] = useState({
    errors: [],
    errorsVisible: false,
    name: "firstName",
    value: "",
  });
  const [lastName, setLastName] = useState({
    errors: [],
    errorsVisible: false,
    name: "lastName",
    value: "",
  });
  const [email, setEmail] = useState({
    errors: [],
    errorsVisible: false,
    fetching: false,
    isUnique: true,
    name: "email",
    value: "",
  })
  const [geolocation, setGeolocation] = useState({
    coordLat: null,
    coordLong: null,
    errors: [],
    name: "geolocation",
    value: false,
  });
  const [password, setPassword] = useState({
    errors: [],
    errorsVisible: false,
    name: "password",
    value: "",
  });
  const [confirmPassword, setConfirmPassword] = useState({
    errors: [],
    errorsVisible: false,
    name: "confirmPassword",
    value: "",
  });
  const [position, setPosition] = useState(0);

  /**
   * Send a request to the API to assert the user's chosen
   * email is not already in use.
   * @param {*} evt DOM event 
   */
  const checkIsEmailUnique = async (evt) => {
    if (window.checkIsEmailUniqueTimeout) {
      clearTimeout(window.checkIsEmailUniqueTimeout);
    }
    if (evt.target.value === "") {
      setEmail({
        ...email,
        errors: [],
        value: "",
      })
      return
    }
    const result = await stateValidation(
      email,
      setEmail,
      { email: emailValidation, },
      evt,
    );
    if (result) {
      setEmail({
        ...email,
        errors: [],
        fetching: true,
      });
      window.checkIsEmailUniqueTimeout = setTimeout(
        () =>
          fetch("/api/users/is_email_unique", {
            method: "POST",
            body: JSON.stringify({
              email: evt.target.value,
            }),
          })
            .then(() =>
              setEmail({
                ...email,
                errors: [],
                fetching: false,
                isUnique: true,
                value: evt.target.value,
              })
            )
            .catch(() =>
              setEmail({
                ...email,
                errors: [],
                fetching: false,
                isUnique: false,
                value: evt.target.value,
              })
            ),
        1000
      );
    }
  };

  // Ask user for full name and email
  const submitBasicInfo = async (evt) => {
    evt.preventDefault();
    const firstNameIsValid = await stateValidation(
      firstName,
      setFirstName,
      { firstName: nameValidation, }
    )
    const lastNameIsValid = await stateValidation(
      lastName,
      setLastName,
      { lastName: nameValidation, }
    )
    const emailIsValid = await stateValidation(
      email,
      setEmail,
      { email: emailValidation, }
    )
    if (
      firstNameIsValid &&
      lastNameIsValid &&
      emailIsValid &&
      email.value.length &&
      email.isUnique &&
      !email.fetching
    ) {
      setPosition(1);
    }
  };

  // Ask user for permission to get device location
  const submitGeolocation = async (evt) => {
    evt.preventDefault();
    const valid = await stateValidation(
      geolocation,
      setGeolocation,
      { geolocation: checkboxValidation }
    )
    if (valid) {
      setPosition(2);
    }
  };

  // Ask a user for a valid password and submit
  const submitSignup = async (evt) => {
    evt.preventDefault();
    const passwordIsValid = await stateValidation(
      password,
      setPassword,
      { password: passwordValidation }
    )
    const confirmPasswordIsValid = password.value === confirmPassword.value
    if (passwordIsValid && confirmPasswordIsValid) {
      await dispatch(
        sessionActions.createNewUser({
          password: password.value,
          firstName: firstName.value,
          lastName: lastName.value,
          email: email.value,
          shareLocation: geolocation.value,
          coordLat: geolocation.coordLat,
          coordLong: geolocation.coordLong,
        })
      )
      setPosition(3)
    }
    else if (!confirmPasswordIsValid) {
      setConfirmPassword({
        ...confirmPassword, errors: [
          "Confirm password does not match."
        ]
      })
    }
  };

  // Get device geolocation and update state
  const getGeolocation = (evt) => {
    evt.preventDefault();
    navigator.geolocation.getCurrentPosition(({ coords }) => {
      setGeolocation((s) => {
        return {
          ...geolocation,
          coordLat: coords.latitude,
          coordLong: coords.longitude,
          value: true,
        };
      });
    });
  };

  return (
    <div className="signup">

      <div className="signup__basic-info">
        <h1>Get your gift on</h1>
        <p>Set up your profile.</p>
        <form onSubmit={submitBasicInfo}>

          <div className={`form-group${firstName.errors.length ? " errors" : ""}`}>
            <label htmlFor="signupFirstNameInput">First name</label>
            <input
              type="text"
              id="signupFirstNameInput"
              disabled={position !== 0}
              onChange={(e) => setFirstName({ ...firstName, value: e.target.value })} />
            {firstName.errors.length ?
              <BsExclamationSquare
                className="form-group__show-errors"
                onClick={() => setFirstName({ ...firstName, errorsVisible: true })} />
              : ""
            }
            {firstName.errorsVisible ?
              <div className="form-group__errors">
                <BsX
                  className="form-group__hide-all-errors"
                  onClick={() => setFirstName({ ...firstName, errorsVisible: false })} />
                {firstName.errors ?
                  <ul>
                    {firstName.errors.map((err, i) => (
                      <li key={`signup-form-first-name-error-${i}`}>{err}</li>
                    ))}
                  </ul> : ""
                }
              </div> : ""
            }
          </div>

          <div className={`form-group${lastName.errors.length ? " errors" : ""}`}>
            <label htmlFor="signupLastNameInput">Last name</label>
            <input
              type="text"
              id="signupLastNameInput"
              disabled={position !== 0}
              onChange={(e) => setLastName({ ...lastName, value: e.target.value })} />
            {lastName.errors.length ?
              <BsExclamationSquare
                className="form-group__show-errors"
                onClick={() => setLastName({ ...lastName, errorsVisible: true })} />
              : ""
            }
            {lastName.errorsVisible ?
              <div className="form-group__errors">
                <BsX
                  className="form-group__hide-all-errors"
                  onClick={() => setLastName({ ...lastName, errorsVisible: false })} />
                {lastName.errors ?
                  <ul>
                    {lastName.errors.map((err, i) => (
                      <li key={`signup-form-last-name-error-${i}`}>{err}</li>
                    ))}
                  </ul> : ""
                }
              </div> : ""
            }
          </div>

          <div className={`form-group${email.errors.length || !email.isUnique ? " errors" : ""}`}>
            <label htmlFor="signupEmailInput">Email</label>
            <input
              type="text"
              id="signupEmailInput"
              disabled={position !== 0}
              onChange={(e) => checkIsEmailUnique(e)} />
            <div className="form-group__email-fetching">
              {email.fetching ?
                <Loader type="bars" color="#000000" /> : ""
              }
            </div>
            <div className="form-group__email-uniqueness">
              {!email.isUnique ?
                <>
                  <p>Email address is already being used by another account.</p>
                  <p>Do you have an account? You can log in <Link to="/login">here!</Link></p>
                </> :
                email.value && !email.errors.length && !email.fetching ?
                  <p>✅</p> : ""
              }
            </div>
            {email.errors.length ?
              <BsExclamationSquare
                className="form-group__show-errors"
                onClick={() => setEmail({ ...email, errorsVisible: true })} />
              : ""
            }
            {email.errorsVisible ?
              <div className="form-group__errors">
                <BsX
                  className="form-group__hide-all-errors"
                  onClick={() => setEmail({ ...email, errorsVisible: false })} />
                {email.errors.length ?
                  <ul>
                    {email.errors.map((err, i) => (
                      <li key={`signup-form-email-error-${i}`}>{err}</li>
                    ))}
                  </ul> : ""
                }
              </div> : ""
            }
          </div>

          <div className="form-group">
            <button
              className="form-group__next-button"
              type="submit"
              disabled={position !== 0}>
              Next...
            </button>
          </div>

        </form>
      </div>

      <div className="signup__share-location">
        <h1>Where are you?</h1>
        <p>
          Surprise Me needs to know your device's location.
          Your location won't be revealed to other people using the app.
        </p>

        <form onSubmit={submitGeolocation}>
          <div className={`form-group${geolocation.errors.length ? " errors" : ""}`}>
            <label htmlFor="signupShareLocationInput">Share my location</label>
            <input
              type="checkbox"
              id="signupShareLocationInput"
              disabled={position !== 1}
              checked={geolocation.value}
              onClick={getGeolocation} />
            <div className="form-group__errors">
              {geolocation.errors ?
                <ul>
                  {geolocation.errors.map((err, i) => (
                    <li key={`signup-form-share-location-error-${i}`}>{err}</li>
                  ))}
                </ul> : ""
              }
            </div>
          </div>

          <div className="form-group">
            <button
              className="form-group__next-button"
              type="submit"
              disabled={position !== 1}>
              Next...
            </button>
            <button
              className="form-group__back-button"
              type="button"
              onClick={() => setPosition(0)}
              disabled={position !== 1}>
              Go back
            </button>
          </div>

        </form>
      </div>
      <div className="signup__set-password">
        <h1>Last step...</h1>
        <p>Choose a password and confirm.</p>

        <form onSubmit={submitSignup}>
          <div className={`form-group${password.errors.length ? " errors" : ""}`}>
            <label htmlFor="signupPasswordInput">Password</label>
            <input
              type="password"
              id="signupPasswordInput"
              disabled={position !== 2}
              onChange={(e) => setPassword({
                ...password,
                value: e.target.value
              })} />
            <div className="form-group__errors">
              {password.errors.length ?
                <ul>
                  {password.errors.map((err, i) => (
                    <li key={`signup-form-password-error-${i}`}>{err}</li>
                  ))}
                </ul> : ""
              }
            </div>
          </div>

          <div className={`form-group${confirmPassword.errors.length ? " errors" : ""}`}>
            <label htmlFor="signupPasswordConfirmInput">Confirm</label>
            <input
              type="password"
              id="signupPasswordConfirmInput"
              disabled={position !== 2}
              onChange={(e) => setConfirmPassword({
                ...confirmPassword,
                value: e.target.value
              })} />
            <div className="form-group__errors">
              {confirmPassword.errors ?
                <ul>
                  {confirmPassword.errors.map((err, i) => (
                    <li key={`signup-form-confirm-password-error-${i}`}>
                      {err}
                    </li>
                  ))}
                </ul> : ""
              }
            </div>
          </div>

          <div className="form-group">
            <button
              className="form-group__next-button"
              type="submit"
              disabled={position !== 2}>
              Sign up
            </button>
            <button
              className="form-group__back-button"
              type="button"
              onClick={() => setPosition(1)}
              disabled={position !== 2}>
              Go back
            </button>
          </div>

        </form>
      </div>
      <div className="signup__success">
        <h2>Welcome to Surprise Me</h2>
        {position === 3 ?
          <Link to="/">Let's get started</Link> : ""
        }
      </div>
      <div className="signup__links">
        <Link to="/login">I have an account</Link>
      </div>
    </div >
  );
};

export default Signup;
