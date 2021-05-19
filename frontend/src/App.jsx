import React, { useEffect, useState } from "react"
import { Switch, Route } from "react-router-dom"
// import { UINotificationOverlay } from "./components/UINotificationOverlay/UINotificationOverlay";

import "./reset.css";
import "./App.css";
import SplashView from "./components/SplashView/SplashView";
import SignUpView from "./components/SignUpView/SignUpView";
import SignInView from "./components/SignInView/SignInView";
import { Authenticated, Anonymous } from "./components/SessionWrapper";

import * as actions from "./store/actions";
import { useDispatch, useSelector } from "react-redux";
import PopupNotifications from "./components/PopupNotifications/PopupNotifications";

const App = () => {
  const session = useSelector(x => x.session);
  const dispatch = useDispatch();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    dispatch(actions.session.getCsrf());
    dispatch(actions.session.get());
  }, []);

  useEffect(() => {
    if (session.timestamp) setMounted(true);
  }, [session.timestamp])

  return !mounted ? null : (
    <PopupNotifications>
      <Switch>
        <Route exact path="/start">
          <Anonymous>
            <SplashView />
          </Anonymous>
        </Route>
        <Route path="/sign-up">
          <Anonymous>
            <SignUpView />
          </Anonymous>
        </Route>
        <Route path="/sign-in">
          <Anonymous>
            <SignInView />
          </Anonymous>
        </Route>
        <Route path="/">
          <Authenticated>
            <h1>AppHome</h1>
          </Authenticated>
        </Route>
      </Switch>
    </PopupNotifications>
  );
};

export default App;
