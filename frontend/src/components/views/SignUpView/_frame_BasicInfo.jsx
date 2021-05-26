/* eslint-disable react/prop-types */

import Loader from "react-loader-spinner";
import React, { useEffect, useState } from "react";

import {
  IoPerson as Person,
  IoMailOpenOutline as Email,
} from "react-icons/io5";

import { ButtonFill } from "../../Buttons";
import { TextInput, EmailInput } from "../../Inputs";
import { useDispatch } from "react-redux";
import * as actions from "../../../store/actions";
import * as validate from "../../_validation";

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
  const [fetching, setFetching] = useState(false);
  const [emailUnique, setEmailUnique] = useState(false);
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
        validation.firstName() &&
        validation.lastName() &&
        validation.email();

      if (valid) {
        setFramePosition(framePosition + 1);
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
  useEffect(() => {
    validation.firstName();
    validation.lastName();
    validation.email();
  }, [firstName.value, lastName.value, email.value]);

  useEffect(() => {
    const errors = [
      ...firstName.errors,
      ...lastName.errors,
      ...email.errors,
      ...(!emailUnique ? ["Email must be unique."] : []),
    ];
    setErrors(errors);
  }, [firstName.errors, lastName.errors, email.errors, emailUnique]);

  useEffect(() => {
    const x = !(
      firstName.value.length &&
      lastName.value.length &&
      emailUnique &&
      email.value.match(emailPattern) &&
      !firstName.errors.length &&
      !lastName.errors.length &&
      !email.errors.length &&
      !fetching &&
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
    fetching,
    framePosition,
  ]);

  useEffect(() => {
    if (framePosition !== 0) setFormDisable(true);
    else setFormDisable(false);
  }, [framePosition]);

  useEffect(() => {
    let timeout;

    clearTimeout(timeout);

    const match = email.value.match(emailPattern);

    if (match) {
      setEmailTried(true);
      setFetching(true);

      timeout = setTimeout(async () => {
        const { payload } = await dispatch(
          actions.user.postEmailUnique({
            email: email.value,
          })
        );

        const { data } = payload;

        setEmailUnique(data);
        setFetching(false);
      }, 500);
    } else setEmailUnique(true);

    return () => clearTimeout(timeout);
  }, [email.value]);

  // ——— element classes ——————————————————————————————————————————————————————
  const classList = {
    fetching: "fetching " + (fetching ? "show" : "hide"),
    emailInUse: "email-in-use " + (emailUnique || fetching ? "hide" : "show"),
  };

  // ——— render ———————————————————————————————————————————————————————————————
  return (
    <div className="frame frame-a">
      <h2>Create an Account</h2>
      <form>
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
      <div className={classList.fetching}>
        <Loader type="TailSpin" color="#555" height={48} width={48} />
      </div>
      <div className={classList.emailInUse}>
        <span>It looks like this email is already in use.</span>
        <span>Do you already have an account?</span>
        <ButtonFill to={`/sign-in?email=${email.value}`} importance="info">
          Sign in
        </ButtonFill>
      </div>
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
