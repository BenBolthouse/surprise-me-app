/* eslint-disable react/prop-types */

import { createElement, Fragment, useEffect, useState } from "react";
import { validate } from "validate.js";

const errorMessages = {
  validatedInputImplementationError:
    "One or more errors occurred while mounting ValidatedInput. ",
  inputImplementationError:
    "One or more errors occurred while mounting Input. ",
};

export function ValidatedInput(props) {
  let { name, state, setState, validation, initialValue, children } = props;

  if (!name) throw Error(errorMessages.inputImplementationError + "name prop is undefined.");
  if (!state) throw Error(errorMessages.inputImplementationError + "state prop is undefined.");
  if (!setState) throw Error(errorMessages.inputImplementationError + "setState prop is undefined.");
  if (!validation.attributes) throw Error(errorMessages.validatedInputImplementationError + "validation prop is missing attributes object.");
  if (!validation.constraints) throw Error(errorMessages.validatedInputImplementationError + "validation prop is missing constraints object.");

  const [stateInitialized, setStateInitialized] = useState(false);

  // Side effect creates the initial state.
  useEffect(() => {
    setState({
      ...state,
      value: initialValue,
      errors: [],
      errorsVisible: false,
    });
    setStateInitialized(true);
  }, []);

  // Side effect runs validation on input changes.
  useEffect(() => {
    if (stateInitialized) {
      const errors = validate(validation.attributes, validation.constraints);

      if (errors) setState({ ...state, errors: Object.values(errors)[0] });
      else setState({ ...state, errors: [] });
    }
  }, [stateInitialized, state.value]);

  return stateInitialized ? createElement(Fragment, null, children) : null;
}

export function Input(props) {
  let { state, setState, initialValue, children } = props;

  if (!state) throw Error(errorMessages.inputImplementationError);
  if (!setState) throw Error(errorMessages.inputImplementationError);

  const [stateInitialized, setStateInitialized] = useState(false);

  // Side effect creates the initial state.
  useEffect(() => {
    setState({
      ...state,
      value: initialValue,
    });
    setStateInitialized(true);
  }, [])

  return stateInitialized ? createElement(Fragment, null, children) : null;
}


