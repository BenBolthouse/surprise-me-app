import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";

import { SignInView, SignUpView } from "./views";

import "./styles/index.css";
import { Anonymous, Authenticated, SessionHandler } from "./components";
import { useDispatch } from "react-redux";
import { actions } from "./store";

const App = () => {
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
    <SessionHandler>
      <Switch>
        <Route exact path="/start/sign-up">
          <Anonymous redirect="/app">
            <SignUpView />
          </Anonymous>
        </Route>
        <Route path="/start">
          <Anonymous redirect="/app">
            <SignInView />
            {/* <StartView /> */}
          </Anonymous>
        </Route>
        <Route path="/app">
          <Authenticated redirect="/start">
            asdf
          </Authenticated>
        </Route>
      </Switch>
    </SessionHandler>
  );
}

export default App;
