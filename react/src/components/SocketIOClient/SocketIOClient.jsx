import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { io } from "socket.io-client";

import * as connectionsActions from "../../store/reducers/connections";
// import * as notificationsActions from "../../store/reducers/notifications";
import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const connectionsTimestamp = useSelector(s => s.connections.timestamp);
  // const notificationsTimestamp = useSelector(s => s.notifications.timestamp);
  const sessionSocketClient = useSelector(s => s.session.socketClient);
  const sessionUser = useSelector(s => s.session.user);

  // Component state
  const [mount, setMount] = useState(false);
  const [socketClientConnected, setSocketClientConnected] = useState(false);
  const isProd = process.env.NODE_ENV === "production"

  useEffect(async () => {
    await dispatch(sessionActions.getSessionUser());
    await dispatch(sessionActions.postSessionGeolocation());
    await dispatch(connectionsActions.getConnections());
  }, [])

  useEffect(async () => {
    if (sessionUser.id && !sessionSocketClient) {
      const transports = isProd ? ["websocket"] : ["polling"];
      const socketio = io("http://localhost:5000").connect({
        transports: transports,
        upgrade: false,
        room: sessionUser.id,
      });
      await dispatch(sessionActions.connectSocketClient(socketio));
    }
    else if (sessionUser && sessionSocketClient && !socketClientConnected) {
      if (!isProd) {
        sessionSocketClient.on("message", (message) => {
          console.log(message);
        });
        sessionSocketClient.on("disconnect", (reason) => {
          console.log("Socketio Client: Client was disconnected:", reason);
        });
      }
      await dispatch(sessionActions.joinSocketClientRoom(sessionUser.id));
      setSocketClientConnected(true);
    }
  }, [sessionUser, sessionSocketClient])

  useEffect(() => {
    if (!mount && sessionUser.id
      && connectionsTimestamp
      && sessionSocketClient) {
      setMount(true);
    }
  })

  return mount ? children : "";
}

export default SocketioRoom;
