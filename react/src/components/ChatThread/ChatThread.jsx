import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";

import * as connectionsActions from "../../store/reducers/connections"
import * as notificationsActions from "../../store/reducers/notifications"
import * as sessionActions from "../../store/reducers/session"

const ChatThread = ({ thread }) => {
  // Hooks
  const dispatch = useDispatch();

  // Component state
  const [message, setMessage] = useState("");
  const otherUser = thread.otherUser;
  const chatHeading = `Messages with ${otherUser.firstName} ${otherUser.lastName}`

  useEffect(() => {
    dispatch(sessionActions.joinSocketClientRoom(thread.id));
    return () => dispatch(sessionActions.leaveSocketClientRoom(thread.id));
  }, [thread]);

  // Event handlers
  const onMessageInputEnterKey = (evt) => {
    if (evt.key === "Enter" || evt.keyCode === 13) {
      evt.preventDefault();
      console.log("Submit event");
    }
  }

  return (
    <div className="chat-thread">
      <h1 className="chat-thread__header">
        {chatHeading}
      </h1>
      <form>
        <textarea onKeyDown={onMessageInputEnterKey}
          onChange={(evt) => setMessage(evt.target.value)} />
      </form>
    </div>
  );
}

export default ChatThread;
