import { useDispatch } from "react-redux";
import { useState } from "react";
import { validate } from "validate.js";

import {
  nameValidation,
  emailValidation,
  passwordValidation,
  requiredValidation,
  checkboxValidation,
  confirmPasswordValidation,
} from "../../validation";

import * as sessionActions from "../../store/reducers/session";
import { Link } from "react-router-dom";

const Signup = () => {
  // Hooks
  const dispatch = useDispatch();

  // Component state
  const [slide1, setSlide1] = useState({
    firstName: "",
    firstNameErrors: [],
    lastName: "",
    lastNameErrors: [],
    email: "",
    emailErrors: [],
  });
  const [slide2, setSlide2] = useState({
    shareLocation: false,
    shareLocationErrors: [],
    coordLat: null,
    coordLong: null,
  });
  const [slide3, setSlide3] = useState({
    password: "",
    passwordErrors: "",
    confirmPassword: "",
    confirmPasswordErrors: "",
  });
  const [slidePosition, setSlidePosition] = useState(0);

  // This hacky bit leverages the
  // convenience of validator.js, which
  // stores validation results as
  // objects with keys.
  // However, since we want errors to
  // exist in arrays on state, a bit of
  // objects key iteration is necessary.
  const validateSlide = (validationObj, schema, state, setStateCallback) => {
    // Errors need to be reset on the
    // onset of validation, or else they
    // will never disappear from state
    // as new fields become valid.
    Object.keys(state).map((key) => {
      if (key.includes("Errors")) {
        state[key] = [];
      }
    });
    const result = validate(validationObj, schema);
    if (result) {
      // If invalid...
      // ...
      // Apply errors to state variable
      // error lists suffixed with
      // "Errors". Return false.
      const convertedErrors = {};
      Object.keys(result).map((key) => {
        convertedErrors[`${key}Errors`] = result[key];
      });
      setStateCallback({ ...state, ...convertedErrors });
      // Return false
      return false;
    }
    // If valid...return true
    return true;
  };

  // Slide 1 validation
  const validateSlide1 = (evt) => {
    evt.preventDefault();
    const vObj = {
      firstName: slide1.firstName,
      lastName: slide1.lastName,
      email: slide1.email,
    };
    const schema = {
      firstName: nameValidation,
      lastName: nameValidation,
      email: emailValidation,
    };
    if (validateSlide(vObj, schema, slide1, setSlide1)) {
      setSlidePosition(1);
    }
  };

  // Slide 2 validation
  const validateSlide2 = (evt) => {
    evt.preventDefault();
    const vObj = {
      shareLocation: slide2.shareLocation,
    };
    const schema = {
      shareLocation: checkboxValidation,
    };
    if (validateSlide(vObj, schema, slide2, setSlide2)) {
      setSlidePosition(2);
    }
  };

  // Slide 3 validation
  const validateSlide3 = (evt) => {
    evt.preventDefault();
    let vObj = {
      password: slide3.password,
      confirmPassword: slide3.confirmPassword,
    };
    const schema = passwordValidation;

    if (validateSlide(vObj, schema, slide3, setSlide3)) {
      submitForm();
    }
  };

  // Handle get geolocation
  const getGeolocation = (evt) => {
    evt.preventDefault();
    navigator.geolocation.getCurrentPosition(({ coords }) => {
      setSlide2((s) => {
        return {
          shareLocation: true,
          coordLat: coords.latitude,
          coordLong: coords.longitude,
        };
      });
    });
  };

  // Form submission
  const submitForm = () => {
    dispatch(
      sessionActions.postSessionUser({
        password: slide3.password,
        firstName: slide1.firstName,
        lastName: slide1.lastName,
        email: slide1.email,
        shareLocation: slide2.shareLocation,
        coordLat: slide2.coordLat,
        coordLong: slide2.coordLong,
      })
    );
  };

  return (
    <div className="signup">
      <div className="signup__basic-info">
        <h1>Get your gift on</h1>

        <p>Set up your profile.</p>

        <form onSubmit={validateSlide1}>
          <div className="form-group">
            <label htmlFor="signupFirstNameInput">First name</label>
            <input
              type="text"
              id="signupFirstNameInput"
              disabled={slidePosition !== 0}
              onChange={(e) =>
                setSlide1({ ...slide1, firstName: e.target.value })
              }
            />
            <div className="form-group__errors">
              {slide1.firstNameErrors && (
                <ul>
                  {slide1.firstNameErrors.map((err, i) => (
                    <li key={`signup-form-first-name-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="signupLastNameInput">Last name</label>
            <input
              type="text"
              id="signupLastNameInput"
              disabled={slidePosition !== 0}
              onChange={(e) =>
                setSlide1({ ...slide1, lastName: e.target.value })
              }
            />
            <div className="form-group__errors">
              {slide1.lastNameErrors && (
                <ul>
                  {slide1.lastNameErrors.map((err, i) => (
                    <li key={`signup-form-last-name-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="signupEmailInput">Email</label>
            <input
              type="text"
              id="signupEmailInput"
              disabled={slidePosition !== 0}
              onChange={(e) => setSlide1({ ...slide1, email: e.target.value })}
            />
            <div className="form-group__errors">
              {slide1.emailErrors && (
                <ul>
                  {slide1.emailErrors.map((err, i) => (
                    <li key={`signup-form-email-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <button type="submit" disabled={slidePosition !== 0}>
              Next...
            </button>
          </div>
        </form>
      </div>
      <div className="signup__share-location">
        <h1>Where are you?</h1>

        <p>
          Surprise Me needs to know where you are. Your location won't be
          revealed to other people using the app.
        </p>

        <form onSubmit={validateSlide2}>
          <div className="form-group">
            <label htmlFor="signupShareLocationInput">Share my location</label>
            <input
              type="checkbox"
              id="signupShareLocationInput"
              disabled={slidePosition !== 1}
              checked={slide2.shareLocation}
              onClick={getGeolocation}
            />
            <div className="form-group__errors">
              {slide2.shareLocationErrors && (
                <ul>
                  {slide2.shareLocationErrors.map((err, i) => (
                    <li key={`signup-form-share-location-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <button type="submit" disabled={slidePosition !== 1}>
              Next...
            </button>
          </div>
        </form>
      </div>
      <div className="signup__set-password">
        <h1>Last step...</h1>

        <p>Choose a password and confirm.</p>

        <form onSubmit={validateSlide3}>
          <div className="form-group">
            <label htmlFor="signupPasswordInput">Password</label>
            <input
              type="password"
              id="signupPasswordInput"
              disabled={slidePosition !== 2}
              onChange={(e) =>
                setSlide3({ ...slide3, password: e.target.value })
              }
            />
            <div className="form-group__errors">
              {slide3.passwordErrors && (
                <ul>
                  {slide3.passwordErrors.map((err, i) => (
                    <li key={`signup-form-password-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="signupPasswordConfirmInput">Confirm</label>
            <input
              type="password"
              id="signupPasswordConfirmInput"
              disabled={slidePosition !== 2}
              onChange={(e) =>
                setSlide3({ ...slide3, confirmPassword: e.target.value })
              }
            />
            <div className="form-group__errors">
              {slide3.confirmPasswordErrors && (
                <ul>
                  {slide3.confirmPasswordErrors.map((err, i) => (
                    <li key={`signup-form-confirm-password-error-${i}`}>{err}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="form-group">
            <button type="submit" disabled={slidePosition !== 2}>
              Finish
            </button>
          </div>
        </form>
      </div>
      <div className="signup__links">
        <Link to="/login">I have an account</Link>
      </div>
    </div>
  );
};

export default Signup;
