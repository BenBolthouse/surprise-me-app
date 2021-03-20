import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { io } from "socket.io-client";

import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const sessionUser = useSelector(s => s.session.user);
  const sessionSocketClient = useSelector(s => s.session.socketClient);

  // Component state
  const isProd = process.env.NODE_ENV === "production"

  useEffect(() => {
    // Create the socketio client on application state
    if (sessionUser && !sessionSocketClient) {
      const transports = isProd ? ["websocket"] : ["polling"];
      const socketio = io("http://localhost:5000").connect({
        transports: transports,
        upgrade: false,
        room: sessionUser.id,
      });
      dispatch(sessionActions.connectSocketClient(socketio));
    }
    // Development logging for socket lifecycle events
    if(!isProd && sessionSocketClient) {
      sessionSocketClient.on("connect", () => {
        console.log("socketio: Client is connected.")
      })
      sessionSocketClient.on("disconnect", (reason) => {
        console.log("socketio: Client was disconnected:", reason)
      })
    }
  }, [sessionSocketClient]);

  // Return the component children
  return children;
}

export default SocketioRoom;
