/* eslint-disable react/prop-types */

import Loader from "react-loader-spinner";
import React, { useEffect, useState } from "react";

import {
  IoPersonOutline as Person,
  IoMailOpenOutline as Email,
} from "react-icons/io5";

import { ButtonFill } from "../../Buttons";
import { TextInput, EmailInput } from "../../Inputs";
import { useDispatch } from "react-redux";
import * as actions from "../../../store/actions";
import * as validate from "../../_validations";

// Styles for individual frames imported on the parent component.
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";

// prettier-ignore
const emailPattern = /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/;

const BasicInfoFrame = ({
  framePosition,
  setFramePosition,
  state,
  setState,
  showErrors,
}) => {
  // ——— hooks ————————————————————————————————————————————————————————————————
  const dispatch = useDispatch();

  // ——— state ————————————————————————————————————————————————————————————————
  const [firstName, setFirstName] = useState({
    value: "",
    errors: [],
  });
  const [lastName, setLastName] = useState({
    value: "",
    errors: [],
  });
  const [email, setEmail] = useState({
    value: "",
    errors: [],
  });
  const [errors, setErrors] = useState([]);
  const [emailUnique, setEmailUnique] = useState(false);
  const [emailFetching, setEmailFetching] = useState(false);
  const [emailTried, setEmailTried] = useState(false);
  const [formDisable, setFormDisable] = useState(false);
  const [nextDisable, setNextDisable] = useState(true);

  // ——— validation ———————————————————————————————————————————————————————————
  const validation = {
    firstName: () => {
      const errors = validate.firstName(firstName.value);
      setFirstName({ ...firstName, errors });

      return errors.length === 0;
    },
    lastName: () => {
      const errors = validate.lastName(lastName.value);
      setLastName({ ...lastName, errors });

      return errors.length === 0;
    },
    email: () => {
      const errors = validate.email(email.value);
      setEmail({ ...email, errors });

      return errors.length === 0;
    },
  };

  // ——— events ———————————————————————————————————————————————————————————————
  const events = {
    firstNameOnChange: (e) => {
      setFirstName({ ...firstName, value: e.target.value });
    },
    lastNameOnChange: (e) => {
      setLastName({ ...lastName, value: e.target.value });
    },
    emailOnChange: (e) => {
      setEmail({ ...email, value: e.target.value });
    },
    formOnSubmit: () => {
      const valid =
        validation.firstName() && validation.lastName() && validation.email();

      if (valid) {
        setFramePosition(1);
        setState({
          ...state,
          firstName: firstName.value,
          lastName: lastName.value,
          email: email.value,
        });
      } else {
        setNextDisable(true);
      }
    },
    errorIconOnClick: () => {
      showErrors(errors);
    },
  };

  // ——— side effects —————————————————————————————————————————————————————————

  // Side effect runs validation on all fields when a change in input value
  // is discovered.
  useEffect(() => {
    validation.firstName();
    validation.lastName();
    validation.email();
  }, [firstName.value, lastName.value, email.value]);

  // Side effect populates the error array when a change in input error
  // value is discovered.
  useEffect(() => {
    const errors = [
      ...firstName.errors,
      ...lastName.errors,
      ...email.errors,
      ...(!emailUnique ? ["Email must be unique."] : []),
    ];

    setErrors(errors);
  }, [firstName.errors, lastName.errors, email.errors, emailUnique]);

  // Side effect handles disabling the "next" button if fields are empty or
  // errors are present.
  useEffect(() => {
    const x = !(
      firstName.value.length &&
      lastName.value.length &&
      emailUnique &&
      email.value.match(emailPattern) &&
      !firstName.errors.length &&
      !lastName.errors.length &&
      !email.errors.length &&
      !emailFetching &&
      framePosition === 0
    );

    setNextDisable(x);
  }, [
    firstName.value,
    firstName.errors,
    lastName.value,
    lastName.errors,
    email.value,
    email.errors,
    emailUnique,
    emailFetching,
    framePosition,
  ]);

  // Side effect simply prevents additional changes to this frame's fields
  // once the user has advanced to another position.
  useEffect(() => {
    if (framePosition !== 0) setFormDisable(true);
  }, [framePosition]);

  // Side effect matches the email value to a regex pattern. If it matches
  // then the "email in use" action is invoked after a half second delay.
  // Depending on the action's return value, an error is added or omitted
  // from the email errors array. This triggers the warning to navigate to
  // sign in, assuming that the user has forgotten that they already have
  // an account.
  useEffect(() => {
    let timeout;

    clearTimeout(timeout);

    const match = email.value.match(emailPattern);

    if (match) {
      setEmailTried(true);
      setEmailFetching(true);

      timeout = setTimeout(async () => {
        const { payload } = await dispatch(
          actions.user.postEmailUnique({
            email: email.value,
          })
        );

        const { data } = payload;

        setEmailUnique(data);
        setEmailFetching(false);
      }, 500);
    } else setEmailUnique(true);

    return () => clearTimeout(timeout);
  }, [email.value]);

  // ——— DOM classes ——————————————————————————————————————————————————————————
  const classList = {
    emailInUse: "email-in-use " + (emailUnique ? "hide" : "show"),
  };

  // ——— render ———————————————————————————————————————————————————————————————
  return (
    <div className="frame frame-a">
      <h2>Create an Account</h2>
      <form autoComplete="chrome-off">
        <TextInput
          icon={<Person />}
          autoFocus={framePosition === 0}
          disabled={formDisable}
          errors={firstName.errors}
          formName="sign-up"
          label="First name"
          name="firstName"
          onChange={events.firstNameOnChange}
          onErrorClick={events.errorIconOnClick}
        />
        <TextInput
          icon={<Person />}
          disabled={formDisable}
          errors={lastName.errors}
          formName="sign-up"
          label="Last name"
          name="lastName"
          onChange={events.lastNameOnChange}
          onErrorClick={events.errorIconOnClick}
        />
        <EmailInput
          icon={<Email />}
          tried={emailTried}
          disabled={formDisable}
          formName="sign-up"
          label="Email"
          name="email"
          onChange={events.emailOnChange}
          onErrorClick={events.errorIconOnClick}
          errors={[
            ...email.errors,
            ...(emailUnique ? [] : ["Email must be unique."]),
          ]}
        />
      </form>
      {emailFetching ? (
        <div className="email-fetching">
          <Loader type="TailSpin" color="#555" height={48} width={48} />
        </div>
      ) : (
          <div className={classList.emailInUse}>
            <span>It looks like this email is already in use.</span>
            <span>Do you already have an account?</span>
            <ButtonFill to={`/sign-in?email=${email.value}`} importance="info">
              Sign in
          </ButtonFill>
          </div>
        )}
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
};

export default BasicInfoFrame;
