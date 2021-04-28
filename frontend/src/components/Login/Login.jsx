import { Link } from "react-router-dom";
import { Loader } from "react-loaders";
import { useDispatch } from "react-redux";
import { useState } from "react";

import * as sessionActions from "../../store/reducers/session";

import "loaders.css/src/animations/ball-pulse.scss";
import "./Login.css";

const Login = () => {
  // Hooks
  const dispatch = useDispatch();

  // Component state
  const [email, setEmail] = useState({
    value: "",
  });
  const [password, setPassword] = useState({
    value: "",
  });
  const [error, setError] = useState(null);
  const [fetching, setFetching] = useState(false);

  // Event handlers
  const onSubmit = async (evt) => {
    evt.preventDefault();
    setFetching(true);
    dispatch(sessionActions.loginSessionUser({
        email: email.value,
        password: password.value,
      }))
      .then(() => setFetching(false))
      .catch((e) => {
        setFetching(false);
        setError(e.data.message);
      });
  };

  return (
    <div className="login">
      <h1>Login</h1>
      <div className="login__error-message">{error}</div>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label htmlFor="loginEmailInput">Email</label>
          <input
            type="text"
            id="loginEmailInput"
            value={email.value}
            onChange={(e) => setEmail({ ...email, value: e.target.value })}
          />
          <label htmlFor="loginPasswordInput">Password</label>
          <input
            type="password"
            id="loginPasswordInput"
            value={password.value}
            onChange={(e) =>
              setPassword({ ...password, value: e.target.value })
            }
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {fetching ?
        <div className="login__fetching-container">
          <div className="login__fetching">
            <Loader type="ball-pulse" color="#ffffff" />
          </div>
        </div> : ""
      }
      <div className="login__register-link">
        <p>
          Don't have an account? <Link to="/signup">Sign up here</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
