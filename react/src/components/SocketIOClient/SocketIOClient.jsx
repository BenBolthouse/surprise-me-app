import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import * as sessionActions from "../../store/reducers/session";

const SocketioRoom = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const sessionUser = useSelector(s => s.session.user);
  const sessionSocketClient = useSelector(s => s.session.socketClient);

  // Side effect set mounted on initial render
  useEffect(() => {
    if (sessionUser && !sessionSocketClient) {
      dispatch(sessionActions.connectSocketClient(sessionUser.id));
    }
    return () => {
      sessionSocketClient.disconnect();
    }
  }, []);

  return children;
}

export default SocketioRoom;
