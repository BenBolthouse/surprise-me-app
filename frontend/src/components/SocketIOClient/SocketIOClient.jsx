import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { io } from "socket.io-client";

import * as chatActions from "../../store/reducers/chat";
import * as connectionsActions from "../../store/reducers/connections";
import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // set locals
  const prd = process.env.NODE_ENV === "production"

  // Hooks
  const dispatch = useDispatch();
  const session = useSelector(s => s.session);
  const connections = useSelector(s => s.connections);
  const sessionUser = useSelector(s => s.session.user);

  // Component state
  const [mount, setMount] = useState(false);
  const [production, setProduction] = useState(prd);

  // ******************************************************
  // side effect establishes universal authenticated user context
  useEffect(() => {
    const dispatchState = async () => {
      await dispatch(sessionActions.patchSessionGeolocation());
      await dispatch(connectionsActions.getConnections());
      await dispatch(connectionsActions.getChatNotifications());
    }
    dispatchState();
  }, []);

  // ******************************************************
  // side effect establishes a connection with the host
  // websocket server and defines application events
  useEffect(() => {
    const sid = sessionUser.id;
    const trs = prd ? ["websocket"] : ["polling"];
    if (sid) {
      const skt = io.connect({
        transports: trs,
        upgrade: false,
        room: sessionUser.id,
      });
      skt.on("chat_message", (msg) => {
        const cid = msg.userConnectionId;
        const snd = msg.sender.id;
        const sid = sessionUser.id;
        if (sid !== snd) {
          dispatch(chatActions.getMessage({
            connId: cid,
            message: msg,
          }));
        }
        dispatch(connectionsActions.updateChatNotification(msg));
      });
      skt.emit("join", { roomId: sid });
      skt.on("composer_interacting", (msg) => {
        dispatch(chatActions.getComposerInteracting(msg));
      });
      if (skt && !production) {
        skt.on("message", (msg) => console.log(msg));
      }
      dispatch(sessionActions.connectSocketClient(skt));
    }
  }, []);

  // ******************************************************
  // side effect prevents premature mounting by stop gating
  // renders before vital state objects are loaded
  useEffect(() => {
    const sid = sessionUser.id;
    const skt = session.socketClient;
    const con = connections.timestamp;
    if (sid && skt && con) setMount(true);
  }, [session, connections]);

  return mount ? children : "";
}

export default SocketioRoom;
