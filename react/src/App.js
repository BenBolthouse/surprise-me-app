import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Route, Switch } from "react-router-dom";
import AuthView from "./components/AuthView/AuthView";

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
    dispatch(sessionActions.getSessionUser());
  }, []);

  return (
    <>
      <Switch>
        <Route path="/signup" exact={true}>
          <AuthView type="Signup" />
        </Route>
        <Route path="/login" exact={true}>
          <AuthView type="Login" />
        </Route>
      </Switch>
    </>
  );
};
