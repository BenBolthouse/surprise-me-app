/* eslint-disable react/prop-types */

import React, { useEffect, useRef, useState } from "react";

import "./sign_up_view.css";
import BasicInfoFrame from "./_frame_BasicInfo";

const SignUpView = () => {
  const frameContainerRef = useRef(null);

  const [position, setPosition] = useState(0);
  const [state, setState] = useState({
    firstName: null,
    lastName: null,
    email: null,
  });

  const props = { position, setPosition, state, setState };

  useEffect(() => {
    frameContainerRef.current.style.left = `-${position * 100}%`;
  }, [position])

  return (
    <div className="view sign-up-view" style={{ left: "0%" }}>
      <div className="center">
        <div className="frame-container" ref={frameContainerRef}>
          <BasicInfoFrame {...props} />




        </div>
      </div>
    </div>
  )
}

export default SignUpView;
