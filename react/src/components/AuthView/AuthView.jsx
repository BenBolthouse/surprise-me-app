import Login from "../Login/Login.jsx";
import Signup from "../Signup/Signup.jsx";

import * as sessionActions from "../../store/reducers/session";
import { useDispatch } from "react-redux";

const AuthView = ({ type }) => {
  // Hooks
  const dispatch = useDispatch();

  const loginAsDemoUserA = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.loginSessionUser({
      "email": "cmeanwell0@t-online.de",
      "password": "Password1234$",
    }));
  }
  const loginAsDemoUserB = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.loginSessionUser({
      "email": "mpitbladdo1@odnoklassniki.ru",
      "password": "Password1234$",
    }));
  }

  return (
    <div className="view auth-view">
      {type === "Signup" ? <Signup /> : ""}
      {type === "Login" ? <Login /> : ""}
      <div className="auth-view__demo-panel">
        <a href="/#" onClick={loginAsDemoUserA}>Login as Demo User A</a>
        <a href="/#" onClick={loginAsDemoUserB}>Login as Demo User B</a>
      </div>
    </div>
  );
};

export default AuthView;
