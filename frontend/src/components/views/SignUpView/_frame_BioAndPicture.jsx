/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */

import React, { useState } from "react";

import {
  IoPersonOutline as Person,
} from "react-icons/io5";

import { ButtonFill, ButtonText } from "../../Buttons";
import { ImageInput } from "../../Inputs";

const acceptableExtensions = [
  "jpg",
  "jpeg",
  "png",
];

const BioAndPictureFrame = ({
  framePosition,
  setFramePosition,
  state,
  setState,
  showErrors,
}) => {

  // ——— state ————————————————————————————————————————————————————————————————
  const [bio, setBio] = useState({
    value: "",
    errors: [],
  });
  const [imagePath, setImagePath] = useState({
    value: "",
    errors: [],
  });
  const [errors, setErrors] = useState([]);
  const [formDisable, setFormDisable] = useState(false);
  const [nextDisable, setNextDisable] = useState(false);
  const [nextText, setNextText] = useState("Skip");

  // ——— events ———————————————————————————————————————————————————————————————
  const events = {
    bioOnChange: (e) => {
      setBio({ ...bio, value: e.target.value });
    },
    imagePathOnChange: (e) => {
      setImagePath({ ...imagePath, value: e.target.value });
    },
    formBackOnClick: () => {
      setFramePosition(framePosition - 1);
    },
    formOnSubmit: () => {
      if (!errors.length) {
        setFramePosition(framePosition + 1);
        setState({
          ...state,
          bio: bio.value,
          imagePath: imagePath.value,
        });
      } else {
        setNextDisable(true);
      }
    },
    errorIconOnClick: () => {
      showErrors(errors);
    },
  };

  return (
    <div className="frame frame-b">
      <h2>Tell Us About You</h2>
      <form autoComplete="chrome-off">
        <ImageInput
          icon={<Person />}
          disabled={formDisable}
          errors={imagePath.errors}
          formName="sign-up"
          label="Profile picture"
          name="imagePath"
          onChange={events.imagePathOnChange}
          onErrorClick={events.errorIconOnClick}
        />
      </form>
      <ButtonText
        onClick={events.formBackOnClick}
      >
        Back
      </ButtonText>
      <ButtonFill
        onClick={events.formOnSubmit}
        disabled={nextDisable}
        importance="info"
      >
        {nextText}
      </ButtonFill>
      <span>Step 3 of 4</span>
    </div>
  );
}

export default BioAndPictureFrame;
