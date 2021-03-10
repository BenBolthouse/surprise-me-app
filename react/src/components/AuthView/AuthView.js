import Login from "../Login/Login";
import Signup from "../Signup/Signup";

const AuthView = ({ type }) => {

  const loginAsDemoUserA = (evt) => {
    evt.preventDefault()
  }
  const loginAsDemoUserB = (evt) => {
    evt.preventDefault()
  }
  
  return (
    <div className="view auth-view">
      {type === "Signup" ? <Signup /> : ""}
      {type === "Login" ? <Login /> : ""}
      <div className="auth-view__demo-panel">
        <a href="#" onClick={loginAsDemoUserA}>Login as Demo User A</a>
        <a href="#" onClick={loginAsDemoUserB}>Login as Demo User B</a>
      </div>
    </div>
  );
};

export default AuthView;
