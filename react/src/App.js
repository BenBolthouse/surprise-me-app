import { useDispatch, useSelector } from "react-redux";

import * as securityActions from "./store/reducers/security";

export default () => {
  // Hooks
  const xCsrfToken = useSelector((s) => s.security.xCsrfToken);
  const dispatch = useDispatch();

  // On every render check if the
  // X-CsrfToken exists. If null then
  // retrieve one.
  if (!xCsrfToken) {
    dispatch(securityActions.getXCsrfToken());
  }

  return <h1>Hello world</h1>;
};
