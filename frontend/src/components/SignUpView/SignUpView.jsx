/* eslint-disable react/prop-types */

import React, { useEffect, useRef, useState } from "react";
import { IoCloseCircleOutline as Close } from "react-icons/io5"

import "./sign_up_view.css";
import BasicInfoFrame from "./_frame_BasicInfo";

const SignUpView = () => {
  const frameContainerRef = useRef(null);

  const [errors, setErrors] = useState([]);
  const [errorsVisible, setErrorsVisible] = useState(false);
  const [position, setPosition] = useState(0);
  const [state, setState] = useState({
    firstName: null,
    lastName: null,
    email: null,
  });

  const showErrors = (errorsArray) => {
    setErrors(errorsArray);
    setErrorsVisible(true);
  };

  const hideErrors = () => {
    setErrors([]);
    setErrorsVisible(false);
  };

  useEffect(() => {
    frameContainerRef.current.style.left = `-${position * 100}%`;
  }, [position])

  const classList = {
    errors: "view errors " + (errorsVisible ? "show" : "hide"),
  }

  const props = { position, setPosition, state, setState, showErrors, hideErrors };

  return (
    <div className="view sign-up-view" style={{ left: "0%" }}>
      <div className={classList.errors} onClick={hideErrors}>
        <div className="center">
          <div className="close"><Close /></div>
          <h2>Please correct the following problems:</h2>
          <ul>
            {errors.map((error, i) => (
              <li key={"sign-up-form-error-" + i}>
                <div className="check">✅</div>
                {error}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="center">
        <div className="frame-container" ref={frameContainerRef}>
          <BasicInfoFrame {...props} />




        </div>
      </div>
    </div>
  )
}

export default SignUpView;
