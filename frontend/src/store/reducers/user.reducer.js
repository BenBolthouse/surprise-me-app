import * as api from "../../fetch";
import userManager from "../models/user.model";

export const getCsrfToken = () => async (dispatch) => {
  const { data } = await api.get("/api/v1/csrf");

  const payload = userManager.update(data);

  return dispatch({ type: "user/GET_CSRF_TOKEN", payload });
};

export const attemptNameAndEmailStep = (props) => {
  const payload = userManager
    .update(props)
    .validate(["firstName", "lastName", "email"]);

  return { type: "user/ATTEMPT_NAME_AND_EMAIL", payload };
};

export const checkEmailIsUnique = (email) => async (dispatch) => {
  const url = "/api/v1/users/check_email_is_unique?email=" + email;

  await api.post(url, {});

  return dispatch({ type: "user/CHECK_EMAIL_IS_UNIQUE" });
};

export const completeNameAndEmailStep = () => {
  const payload = userManager
    .completeNameAndEmail(userManager.validation.passed);

  return { type: "user/COMPLETE_NAME_AND_EMAIL", payload };
};

export const attemptPictureAndBioStep = (props) => {
  const payload = userManager.update(props)

  return { type: "user/ATTEMPT_PICTURE_AND_BIO", payload };
};

export const completePictureAndBioStep = () => {
  const payload = userManager
    .completePictureAndBio(userManager.validation.passed);

  return { type: "user/COMPLETE_PICTURE_AND_BIO", payload };
};

export const attemptGeolocationStep = (props) => {
  const payload = userManager
    .update(props)
    .validate(["latitude", "longitude"]);

  return { type: "user/ATTEMPT_GEOLOCATION", payload };
};

export const completeGeolocationStep = () => {
  const payload = userManager
    .completeGeolocation(userManager.validation.passed);

  return { type: "user/COMPLETE_GEOLOCATION", payload };
};

export const attemptPasswordStep = (props) => {
  const payload = userManager
    .update(props)
    .validate(["password", "confirmPassword"]);

  return { type: "user/ATTEMPT_PASSWORD", payload };
};

export const completePasswordStep = () => {
  const payload = userManager
    .completePassword(userManager.validation.passed);

  return { type: "user/COMPLETE_PASSWORD", payload };
};

export const postUser = () => async (dispatch) => {
  const url = "/api/v1/users"

  const { data } = await api.post(url, userManager.returnProps());

  const payload = userManager.update(data || {});

  return dispatch({ type: "user/POST_USER", payload });
};

export const getUser = () => async (dispatch) => {
  const { data } = await api.get("/api/v1/sessions");

  const payload = userManager.update(data || {});

  return dispatch({ type: "user/GET_USER", payload });
};

export const signInUser = (props) => async (dispatch) => {
  const { data } = await api.post("/api/v1/sessions", props)

  const payload = userManager.update(data || {});

  return dispatch({ type: "user/SIGN_USER_IN", payload });
};

const reducer = (_state, { type }) => {
  switch (type) {
    default:
      return userManager.return();
  }
};

export default reducer;
