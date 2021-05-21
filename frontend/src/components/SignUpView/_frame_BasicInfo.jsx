/* eslint-disable react/prop-types */

import React, { useEffect, useState } from "react";
import {
  IoPersonOutline as Person,
  IoMailOpenOutline as Email,
} from "react-icons/io5"

import { ButtonFill, ButtonText } from "../Buttons/Buttons";
import TextInput from "../Inputs/TextInputs";
import * as validate from "./_validations";
import * as actions from "../../store/actions";
import { useDispatch } from "react-redux";

const BasicInfoFrame = ({
  position,
  setPosition,
  state: parentState,
  setState: setParentState,
}) => {
  const dispatch = useDispatch();

  const [state, setState] = useState({
    firstName: {
      value: "",
      errors: [],
    },
    lastName: {
      value: "",
      errors: [],
    },
    email: {
      value: "",
      errors: [],
      uniqueError: [],
    },
    inputsDisabled: false,
    nextDisabled: true,
  });

  const validation = {
    firstName: () => {
      const copy = { ...state };
      copy.firstName.errors = validate.firstName(copy.firstName.value);
      setState(copy);

      return copy.firstName.errors.length === 0;
    },
    lastName: () => {
      const copy = { ...state };
      copy.lastName.errors = validate.lastName(copy.lastName.value);
      setState(copy)

      return copy.lastName.errors.length === 0;
    },
    email: () => {
      const copy = { ...state };
      copy.email.errors = validate.email(copy.email.value);
      setState(copy);

      return copy.email.errors.length === 0;
    },
  }

  const events = {
    firstNameOnChange: (e) => {
      const copy = { ...state };
      copy.firstName.value = e.target.value;
      setState(copy);

      validation.firstName();
    },
    lastNameOnChange: (e) => {
      const copy = { ...state };
      copy.lastName.value = e.target.value;
      setState(copy);

      validation.lastName();
    },
    emailOnChange: (e) => {
      const copy = { ...state };
      copy.email.value = e.target.value;
      setState(copy);

      validation.email();
    },
    formOnSubmit: () => {
      const copy = { ...state };

      const valid =
        validation.firstName() &&
        validation.lastName() &&
        validation.email();

      if (valid) {
        const { firstName, lastName } = copy;
        setPosition(1);
        setParentState({
          ...parentState,
          firstName: firstName.value,
          lastName: lastName.value,
        });
      }
      else {
        setState({
          ...state,
          nextDisabled: true,
        });
      }
    },
  }

  useEffect(() => {
    const copy = { ...state };

    copy.nextDisabled =
      !(state.firstName.value.length &&
        state.lastName.value.length &&
        state.email.value.length &&
        position === 0);

    setState(copy);
  }, [
    state.firstName.value,
    state.lastName.value,
    state.email.value,
    position
  ]);

  useEffect(() => {
    if (position !== 0) setState({
      ...state,
      inputsDisabled: true,
    });
  }, [position])

  useEffect(() => {
    let timeout;

    const copy = { ...state };

    let match = /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?/.()<>[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d-]+(?:\.[a-zA-Z\d-]+)*\.[a-zA-Z].{1,4})$/;

    match = state.email.value.match(match)


    if (match) {
      timeout = setTimeout(async () => {
        const { payload: unique } = await dispatch(actions.user.postEmailUnique({
          email: copy.email.value,
        }));

        if (!unique) copy.email.uniqueError = ["Email must be unique."];
        else if (unique) copy.email.uniqueError = [];

        setState(copy);
      }, 1000)
    }
    else {
      copy.email.uniqueError = [];

      setState(copy);
    }

    return () => clearTimeout(timeout);
  }, [state.email.value])

  const classList = {
    emailInUse: () => {
      return state.email.uniqueError.length ? "show" : "hide";
    }
  }

  return (
    <div className="frame frame-a">
      <h2>Create an Account</h2>
      <form>
        <TextInput
          icon={<Person />}
          onChange={events.firstNameOnChange}
          onBlur={null}
          onErrorClick={null}
          errors={state.firstName.errors}
          name="first-name"
          formName="sign-up"
          label="First name" />
        <TextInput
          icon={<Person />}
          onChange={events.lastNameOnChange}
          onBlur={null}
          onErrorClick={null}
          errors={state.lastName.errors}
          name="last-name"
          formName="sign-up"
          label="Last name" />
        <TextInput
          icon={<Email />}
          onChange={events.emailOnChange}
          onBlur={null}
          onErrorClick={null}
          errors={[
            ...state.email.errors,
            ...state.email.uniqueError,
          ]}
          name="email"
          formName="sign-up"
          label="Email" />
      </form>
      <div className={"email-in-use " + classList.emailInUse()}>
        <span>It looks like this email is already in use.</span>
        <span>Do you already have an account?</span>
        <ButtonFill
          to={`/sign-in?email=${state.email.value}`}
          importance="info">
          Sign in
      </ButtonFill>
      </div>
      <ButtonText
        onClick={events.formOnSubmit}
        disabled={state.nextDisabled}
        importance="info">
        Next
      </ButtonText>
      <span>Step 1 of 4</span>
    </div>
  )
};

export default BasicInfoFrame;
