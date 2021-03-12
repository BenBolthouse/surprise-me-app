import { useEffect } from "react";

/**
 * Wraps a high-order component to provide a five-second
 * beat to access state changes on the backend API.
 * @param {*} props React props
 */
const HeartbeatApiAccess = ({ children }) => {
  console.log("Heartbeat begin...")

  useEffect(() => {
    window.heartbeatApiAccess = setInterval(() => {

    })
  }, [])
  return children;
}

export default HeartbeatApiAccess;
