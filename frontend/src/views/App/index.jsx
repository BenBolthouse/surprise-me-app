/* eslint-disable no-unused-vars */

import { Switch, Route } from "react-router-dom";
import { useDispatch } from "react-redux";
import React, { useEffect, useState } from "react";

import { SignInView, SignUpView, StartView } from "..";

import { actions } from "../../store";

import "./styles/index.css";

export function App() {
  const dispatch = useDispatch();

  const [mounted, setMounted] = useState(false);

  // Side effect awaits retrieval of data and then sets the component state
  // to mounted.
  useEffect(() => {
    async function go() {
      await dispatch(actions.session.getCsrf());
    }
    go();

    setMounted(true);
  }, [])

  return !mounted ? null : (
    <Switch>
      <Route exact path={["/start/sign-up"]}>
        <SignUpView />
      </Route>
      <Route exact path={["/start", "/start/sign-in"]}>
        <SignInView />
        <StartView />
      </Route>
      <Route path="/app">
        asdf
      </Route>
    </Switch>
  );
}
