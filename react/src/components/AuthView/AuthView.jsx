import Login from "../Login/Login.jsx";
import Signup from "../Signup/Signup.jsx";
import { useDispatch } from "react-redux";

import * as sessionActions from "../../store/reducers/session";

import "./AuthView.css";

const AuthView = ({ children }) => {
  // Hooks
  const dispatch = useDispatch();

  const loginA = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.loginSessionUser({
      "email": "cmeanwell0@t-online.de",
      "password": "Password1234$",
    }));
  }
  const loginB = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.loginSessionUser({
      "email": "mpitbladdo1@odnoklassniki.ru",
      "password": "Password1234$",
    }));
  }

  return (
    <div className="view auth-view">
      <div className="center">
        {children}
      </div>
      <div className="demo">
        <button onClick={loginA}>Login as Demo User A</button>
        <button onClick={loginB}>Login as Demo User B</button>
      </div>
    </div>
  );
};

export default AuthView;
