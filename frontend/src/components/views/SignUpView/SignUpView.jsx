/* eslint-disable react/prop-types */

import React, { useEffect, useRef, useState } from "react";
import { IoCloseCircleOutline as Close } from "react-icons/io5";

import "./sign_up_view.css";
import BasicInfoFrame from "./_frame_BasicInfo";
import BioAndPictureFrame from "./_frame_BioAndPicture";
import PasswordFrame from "./_frame_Password";

const SignUpView = () => {
  const frameContainerRef = useRef(null);

  const [state, setState] = useState({
    firstName: null,
    lastName: null,
    email: null,
    password: null,
  });
  const [errors, setErrors] = useState([]);
  const [errorsVisible, setErrorsVisible] = useState(false);
  const [framePosition, setFramePosition] = useState(2);

  // ——— events ———————————————————————————————————————————————————————————————
  const events = {
    errorsOpenOnClick: (errorsArray) => {
      setErrors(errorsArray);
      setErrorsVisible(true);
    },
    errorsCloseOnClick: () => {
      setErrors([]);
      setErrorsVisible(false);
    },
  };

  useEffect(() => {
    frameContainerRef.current.style.left = `-${framePosition * 100}%`;
  }, [framePosition]);

  const classList = {
    errors: "view errors " + (errorsVisible ? "show" : "hide"),
  };

  const props = {
    framePosition,
    setFramePosition,
    state,
    setState,
    showErrors: events.errorsOpenOnClick,
    hideErrors: events.errorsCloseOnClick,
  };

  return (
    <div className="view sign-up-view" style={{ left: "0%" }}>
      <div className={classList.errors} onClick={events.errorsCloseOnClick}>
        <div className="center">
          <div className="close">
            <Close />
          </div>
          <h2>Please correct the following:</h2>
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
          <PasswordFrame {...props} />
          <BioAndPictureFrame {...props} />
        </div>
      </div>
    </div>
  );
};

export default SignUpView;
