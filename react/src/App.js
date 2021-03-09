import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

export default () => {
  // Hooks
  const xCsrfToken = useSelector((s) => s.security.xCsrfToken);
  const dispatch = useDispatch();

  useEffect(() => {
    // On every render check if the
    // X-CsrfToken exists. If null then
    // retrieve one.
    if (!xCsrfToken) {
      dispatch(securityActions.getXCsrfToken());
    }

    // On every render attempt to get
    // the session user.
    dispatch(sessionActions.getSessionUser())
  }, []);

  return <h1>Hello world</h1>;
};
