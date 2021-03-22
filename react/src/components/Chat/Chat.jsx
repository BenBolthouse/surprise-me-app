import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { NavLink, useParams } from "react-router-dom";

import ChatThread from "../ChatThread/ChatThread";

import "./Chat.css";

const Chat = () => {
  // URL slug
  const { slug } = useParams()

  // Hooks
  const connections = useSelector(s => s.connections);

  // Component state
  const [activeMessageThreads, setActiveMessageThreads] = useState(null);

  useEffect(() => {
    const messageThreads = [];
    // eslint-disable-next-line no-unused-vars
    for (const [key, value] of Object.entries(connections.established)) {
      if (value.lastChatMessageDatetime) messageThreads.push(value);
    }
    setActiveMessageThreads(messageThreads);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [connections.established]);

  return (
    <div className="chat-viewport-container">
      <div className="view chat-view">
        <div className="chat__mobile-nav">

        </div>
        <div className="chat__sidebar">
          <ul className="chat__threads-available">
            {activeMessageThreads ?
              <>
                {activeMessageThreads.map(messageThread => (
                  <ThreadAvailable
                    key={`active-message-thread-${messageThread.id}`}
                    thread={messageThread} />
                ))}
              </> : ""
            }
          </ul>
        </div>
        {slug !== "start" ?
          <div className="chat__thread-container">
            <ChatThread />
          </div> :
          <div className="chat__splash-container">
            <div className="chat__splash">
              <h1>Messages</h1>
              <p>Select or search for a friend to start a conversation.</p>
            </div>
          </div>
        }
      </div>
    </div>
  );
}

const ThreadAvailable = ({ thread }) => {
  const otherUserName = `${thread.otherUser.firstName} ${thread.otherUser.lastName}`;
  const otherUserThumbnail = `/f/profile_${thread.otherUser.id}_64p.jpg`;
  const otherUserThumbAlt = `User ${thread.otherUser.id} profile picture`;
  const threadUrl = `/messages/${thread.id}`;
  return (
    <NavLink to={threadUrl}>
      <li>
        <img src={otherUserThumbnail} alt={otherUserThumbAlt} />
        <p>{otherUserName}</p>
      </li>
    </NavLink>
  )
}

export default Chat;
