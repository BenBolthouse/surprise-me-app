import { Link } from "react-router-dom"

const Login = () => {
  return(
    <div className="login">
      Don't have an account? <Link to="/signup">Sign up here</Link>
      LOGIN
    </div>
  )
}

export default Login
