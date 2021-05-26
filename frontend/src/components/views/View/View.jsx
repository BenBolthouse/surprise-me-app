/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */

import { IoCloseCircleOutline as Close } from "react-icons/io5";
import Loader from "react-loader-spinner";
import React, { useState } from "react";

import "./view.css";

const View = ({ children, name }) => {
  const [errors, setErrors] = useState([]);
  const [showErrors, setShowErrors] = useState(false);
  const [awaiting, setAwaiting] = useState(false);

  const props = {
    viewSetErrors: setErrors,
    viewShowErrors: setShowErrors,
    viewSetAwaiting: setAwaiting,
  };

  const viewClasses = "view " + name + "-view";
  const viewErrorsClasses = "view-errors " + (showErrors && errors.length ? "show" : "hide");
  const viewAwaitingClasses = "view-awaiting " + (awaiting ? "show" : "hide");

  return (
    <div className={viewClasses}>
      <div className={viewErrorsClasses}>
        <center>
          <div className="close">
            <Close />
          </div>
          <h2>Please correct the following:</h2>
          <ul>
            {errors.map((error, i) => (
              <li key={name + "-view-error-" + i}>{error}</li>
            ))}
          </ul>
        </center>
      </div>
      <div className={viewAwaitingClasses}>
        <center>
          <Loader type="Oval" />
        </center>
      </div>
      <div className="view-content">
        <center>
          {React.cloneElement(children, { ...children.props, ...props })}
        </center>
      </div>
    </div>
  );
};

export default View;
