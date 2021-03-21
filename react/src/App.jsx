import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, Route, Switch } from "react-router-dom";

import AuthView from "./components/AuthView/AuthView.jsx";
import Chat from "./components/Chat/Chat.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import UnauthSplash from "./components/UnauthSplash/UnauthSplash.jsx";
import SocketioRoom from "./components/SocketIOClient/SocketIOClient.jsx";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

import "./reset.css";
import "./App.css";

const App = () => {
  // Hooks
  const sessionUser = useSelector((s) => s.session.user)
  const modalComponent = useSelector((s) => s.modal.component)
  const dispatch = useDispatch();

  // Component state
  const [mount, setMount] = useState(false);

  useEffect(() => {
    const dispatchState = async () => {
      await dispatch(securityActions.getXCsrfToken());
      await dispatch(sessionActions.getSessionUser())
        .then(() => setMount(true))
        .catch(() => setMount(true));
    }
    dispatchState()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch]);

  return (
    <>
      {mount ?
        <div className="view-container">
          {modalComponent ?
            modalComponent.map(modal => (
              <div key="modal">
                {modal}
              </div>
            )) : ""
          }
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
              {sessionUser.id ?
                <SocketioRoom>
                  <Navbar />
                  <Route exact path="/">
                    HOME
                  </Route>
                  <Route exact path="/messages">
                    <Redirect to="/messages/start" />
                  </Route>
                  <Route path="/messages/:slug">
                    <Chat />
                  </Route>
                </SocketioRoom> :
                <UnauthSplash />
              }
            </Route>
            <Route to="*">
              404!!!
            </Route>
          </Switch>
        </div> : ""}
    </>
  );
};

export default App;
