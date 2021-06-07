import React from "react";
import { Switch, Route } from "react-router-dom";

import { SignInView, SignUpView, StartView } from "./views";

const App = () => {
  return (
    <Switch>
      <Route exact path="/start/sign-up">
        <SignUpView />
      </Route>
      <Route path="/start">
        <SignInView />
        <StartView />
      </Route>
      <Route path="/app">
      </Route>
    </Switch>
  );
}

export default App;
