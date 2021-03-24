import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, Route, Switch, useLocation } from "react-router-dom";

import AuthView from "./components/AuthView/AuthView.jsx";
import Chat from "./components/Chat/Chat.jsx";
import Login from "./components/Login/Login.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import Signup from "./components/Signup/Signup.jsx";
import SocketioRoom from "./components/SocketIOClient/SocketIOClient.jsx";
import UnauthSplash from "./components/UnauthSplash/UnauthSplash.jsx";

import * as securityActions from "./store/reducers/security";
import * as sessionActions from "./store/reducers/session";

import "./reset.css";
import "./App.css";

const App = () => {
  // Hooks
  const sessionUser = useSelector((s) => s.session.user)
  const modalComponent = useSelector((s) => s.modal.component)
  const dispatch = useDispatch();
  const location = useLocation();

  // Component state
  const [mount, setMount] = useState(false);

  useEffect(() => {
    dispatch(sessionActions.getSessionUser())
      .then(() => setMount(true))
      .catch(() => setMount(true));
  }, [dispatch]);

  useEffect(() => {
    dispatch(securityActions.getXCsrfToken());
  }, [location])

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
              <AuthView>
                <Signup />
              </AuthView>
            </Route>
            <Route exact path="/login">
              {sessionUser.id ?
                <Redirect to="/" /> :
                <AuthView>
                  <Login />
                </AuthView>
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
        </div> : ""
      }
    </>
  );
};

export default App;
