import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, Route, Switch } from "react-router-dom";

import AuthView from "./components/AuthView/AuthView.jsx";
import Chat from "./components/Chat/Chat.jsx";
import ChatThread from "./components/ChatThread/ChatThread.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import UnauthSplash from "./components/UnauthSplash/UnauthSplash.jsx";
import SocketioRoom from "./components/SocketIOClient/SocketIOClient.jsx";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

import "./reset.css";
import "./App.css";

const App = () => {
  // Hooks
  const xCsrfToken = useSelector((s) => s.security.xCsrfToken);
  const sessionUser = useSelector((s) => s.session.user)
  const modalComponent = useSelector((s) => s.modal.component)
  const dispatch = useDispatch();

  useEffect(() => {
    if (!xCsrfToken) {
      dispatch(securityActions.getXCsrfToken());
    }
  }, [dispatch]);

  return (
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
          </SocketioRoom>
        </Route>
        <Route to="*">
          404!!!
        </Route>
      </Switch>
    </div>
  );
};

export default App;
