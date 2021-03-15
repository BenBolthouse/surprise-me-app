import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";

import * as connectionsActions from "../../store/reducers/connections"
import * as notificationsActions from "../../store/reducers/notifications"

const ChatThread = () => {
  // Hooks
  const dispatch = useDispatch();
  const sessionUser = useSelector(s => s.session.user);
  const connections = useSelector(s => s.connections)

  // Component state
  const [thread, setThread] = useState(null)

  // Get the connection id from the URL
  const { slug } = useParams();
  const connectionId = parseInt(slug)

  // Component state
  const [mount, setMount] = useState(false);
  const [composeText, setComposeText] = useState("");

  // Side effect get the thread from the connection ID found
  // in the URL path. Delete notifications about unread
  // messages for this thread, which are now unneeded.
  useEffect(() => {
    if (connections.datestamp) {
      setMount(true);
      setThread(connections.established[connectionId])
      dispatch(notificationsActions.deleteChatNotification(connectionId))
    };
  }, [slug, connections])

  // Refs
  const scrollIntoViewRef = useRef(null)
  const composeFormRef = useRef(null)

  useEffect(() => {
    if (scrollIntoViewRef.current) scrollIntoViewRef.current.scrollIntoView();
  });

  // Handle send message
  const submitComposeMessage = (evt) => {
    evt.preventDefault();
    dispatch(connectionsActions.postConnectionMessage({
      connectionId,
      senderUserId: sessionUser.id,
      senderUserFirstName: sessionUser.firstName,
      senderUserLastName: sessionUser.lastName,
      body: composeText,
    }))
    setComposeText("")
  }

  return (
    <>
      {mount ?
        <div className="chat-thread">

          <div className="chat-thread__top-bar">
            <h2>Your messages with {thread.connectionFirstName}</h2>
          </div>

          <div className="chat-thread__body">
            {thread.messages.map((message, i) => (
              <ChatFrame
                message={message}
                key={`chat-frame-conn-${thread.id}-msg-${message.id}`} />
            ))}
            <div ref={scrollIntoViewRef} id="chatThreadScrollIntoView"></div>
          </div>

          <div className="chat-thread__compose">
            <form ref={composeFormRef} onSubmit={submitComposeMessage}>
              <input
                type="text"
                id="chatThreadComposeText"
                value={composeText}
                onChange={(evt) => setComposeText(evt.target.value)} />
              <button type="submit">Send</button>
            </form>
          </div>

        </div> : ""}
    </>
  );
}

const ChatFrame = ({ message }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user)

  // Props
  const { senderUserFirstName, senderUserLastName,
    senderUserId, body, createdAt, } = message

  // Convert datetime to a readable format
  const sentAt = new Date(createdAt).toDateString();

  // For use in styling according to who sent the message
  const type = sessionUser.id === senderUserId
    ? "sent"
    : "received"

  return (
    <div className={`chat-message ${type}`}>
      <h3>{`${senderUserFirstName} ${senderUserLastName}`}</h3>
      <p>{body}</p>
      <div className="chat-message__sent-at">{sentAt}</div>
    </div>
  )
}

export default ChatThread;
