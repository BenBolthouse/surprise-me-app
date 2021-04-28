import { useDispatch } from "react-redux";

import * as sessionActions from "../../store/reducers/session";

import "./AuthView.css";
import { useHistory } from "react-router-dom";

const AuthView = ({ children }) => {
  // Hooks
  const dispatch = useDispatch();
  const history = useHistory();

  const loginA = async (evt) => {
    evt.preventDefault()
    await dispatch(sessionActions.loginSessionUser({
      "email": "cmeanwell0@t-online.de",
      "password": "Password1234$",
    }));
    history.push("/");
  }
  const loginB = async (evt) => {
    evt.preventDefault()
    await dispatch(sessionActions.loginSessionUser({
      "email": "gbogace3@cbc.ca",
      "password": "Password1234$",
    }));
    history.push("/");
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
