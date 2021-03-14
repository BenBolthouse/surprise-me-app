import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";

const ChatThread = () => {
  // Hooks
  const { slug } = useParams();
  const thread = useSelector(s => s.connections.established.connections[parseInt(slug)])

  // Component state
  const [mount, setMount] = useState(false);

  // Handle mounting
  useEffect(() => {
    if (thread) setMount(true);
  }, [thread])

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
                key={`chat-frame-conn-${thread.id}-msg-${i}`} />
            ))}
          </div>

        </div> : ""}
    </>);
}

const ChatFrame = ({ message }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user)

  // Props
  const { senderUserFirstName, senderUserLastName,
    senderUserId, body, createdAt, } = message

  // Convert datetime
  let sentAt = Date.parse(createdAt)
  sentAt = new Date().toDateString(sentAt)

  // Style according to sender versus recipient
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
