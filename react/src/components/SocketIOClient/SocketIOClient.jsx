import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { io } from "socket.io-client";

import * as chatActions from "../../store/reducers/chat";
import * as connectionsActions from "../../store/reducers/connections";
import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const connectionsTimestamp = useSelector(s => s.connections.timestamp);
  const sessionSocketClient = useSelector(s => s.session.socketClient);
  const sessionUser = useSelector(s => s.session.user);

  // Component state
  const [mount, setMount] = useState(false);
  const [socketClientConnected, setSocketClientConnected] = useState(false);
  const isProd = process.env.NODE_ENV === "production"

  useEffect(() => {
    const dispatchState = async () => {
      await dispatch(sessionActions.patchSessionGeolocation());
      await dispatch(connectionsActions.getConnections());
    }
    dispatchState();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (sessionUser.id && !sessionSocketClient) {
      const transports = isProd ? ["websocket"] : ["polling"];
      const socketio = io.connect({
        transports: transports,
        upgrade: false,
        room: sessionUser.id,
      });
      const dispatchConnectSocketClient = async () => {
        await dispatch(sessionActions.connectSocketClient(socketio));
      }
      dispatchConnectSocketClient();
    }
    else if (sessionUser && sessionSocketClient && !socketClientConnected) {
      if (!isProd) {
        sessionSocketClient.on("chat_message", (message) => {
          console.log(message);
        });
        sessionSocketClient.on("disconnect", (reason) => {
          console.log("Socketio Client: Client was disconnected:", reason);
        });
        sessionSocketClient.on("messages", (payload) => {
          console.log("Socketio Client: Message received:", payload);
        });
      }
      sessionSocketClient.on("composer_interacting", (payload) => {
        if (payload.interacting) {
          dispatch(chatActions.postComposerInteracting(payload.roomId))
        }
        else {
          dispatch(chatActions.deleteComposerInteracting(payload.roomId))
        }
      })
      sessionSocketClient.on("chat_message", (payload) => {
        if (payload.sender.id !== sessionUser.id) {
          dispatch(chatActions.getMessage({
            connId: payload.userConnectionId,
            message: payload,
          }));
        }
      })
      dispatch(sessionActions.joinSocketClientRoom(sessionUser.id));
      setSocketClientConnected(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
