import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Route, Switch } from "react-router-dom";

import AuthView from "./components/AuthView/AuthView.jsx";
import Chat from "./components/Chat/Chat.jsx";
import ChatThread from "./components/ChatThread/ChatThread.jsx";
import HeartbeatApiAccess from "./components/HeartbeatApiAccess/HeartbeatApiAccess.jsx";
import UnauthSplash from "./components/UnauthSplash/UnauthSplash.jsx";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

const App = () => {
  // Hooks
  const xCsrfToken = useSelector((s) => s.security.xCsrfToken);
  const sessionUser = useSelector((s) => s.session.user)
  const dispatch = useDispatch();

  // State
  const [mounted, setMounted] = useState(false)

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
      .then(() => setMounted(true))
      .catch(() => setMounted(true));
  }, [dispatch]);

  return (
    <>
      <Switch>
        <Route path="/">
          {mounted ?
            sessionUser.id ?
              <>
                <HeartbeatApiAccess>
                  <Route path="/messages/:slug">
                    <Chat>
                      <ChatThread />
                    </Chat>
                  </Route>
                </HeartbeatApiAccess>
              </> :
              <UnauthSplash />
            : ""
          }
        </Route>
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

export default App;
