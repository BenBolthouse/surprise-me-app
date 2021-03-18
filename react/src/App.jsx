import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, Route, Switch } from "react-router-dom";

import AuthView from "./components/AuthView/AuthView.jsx";
import Chat from "./components/Chat/Chat.jsx";
import ChatThread from "./components/ChatThread/ChatThread.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import UnauthSplash from "./components/UnauthSplash/UnauthSplash.jsx";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

import "./reset.css";
import "./App.css";

const App = () => {
  // Hooks
  const xCsrfToken = useSelector((s) => s.security.xCsrfToken);
  const sessionUser = useSelector((s) => s.session.user)
  const dispatch = useDispatch();

  // Component state
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
    <div className="view-container">
      <Switch>
        <Route exact path="/signup">
          {sessionUser.id ?
            <Redirect to="/" /> :
            <AuthView type="Signup" />
          }
        </Route>
        <Route exact path="/login">
          {sessionUser.id ?
            <Redirect to="/" /> :
            <AuthView type="Login" />
          }
        </Route>
        <Route path="/">
          <>
            {mounted ?
              <>
                {sessionUser.id ?
                  <>
                    <Navbar />
                    <>
                      <Route path="/messages">
                        <Chat>
                          <Route path="/messages/:slug">
                            <ChatThread />
                          </Route>
                        </Chat>
                      </Route>
                      <Route to="*">
                        404!!!
                    </Route>
                    </>
                  </> : <UnauthSplash />
                }
              </> : <Redirect push to="/" />
            }
          </>
        </Route>
      </Switch>
    </div>
  );
};

export default App;
