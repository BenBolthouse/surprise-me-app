import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { io } from "socket.io-client";

import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const sessionUser = useSelector(s => s.session.user);
  const sessionSocketClient = useSelector(s => s.session.socketClient);


  // Side effect set mounted on initial render
  useEffect(() => {
    if (sessionUser && !sessionSocketClient) {
      // Socketio client configuration
      const socketio = io("http://localhost:5000").connect({
        transports: ["polling", "websocket"]
      });

      // Add client to app state
      dispatch(sessionActions.connectSocketClient(socketio));
    }

    // Disconnect socket client on cleanup
    return () => {
      socketio.disconnect();
      // TODO add dispatch to remove from Redux 
    }
  }, [sessionSocketClient]);

  // Return the component children
  return children;
}

export default SocketioRoom;
