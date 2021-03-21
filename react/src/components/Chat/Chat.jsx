import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { NavLink, useParams } from "react-router-dom";

import ChatThread from "../ChatThread/ChatThread";

import "./Chat.css";

const Chat = () => {

  // URL slug
  const { slug } = useParams()

  // Hooks
  const connections = useSelector(s => s.connections);

  // Component state
  const [scopedMessageThread, setScopedMessageThread] = useState(null);
  const [activeMessageThreads, setActiveMessageThreads] = useState(null);

  useEffect(() => {
    const messageThreads = [];
    // eslint-disable-next-line no-unused-vars
    for (const [key, value] of Object.entries(connections.established)) {
      if (value.lastChatMessageDatetime) messageThreads.push(value);
    }
    setActiveMessageThreads(messageThreads);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (slug === "start") setScopedMessageThread(null);
    else setScopedMessageThread(connections.established[slug]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug, connections.established]);

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
                    threadId={messageThread.id}
                    otherUser={messageThread.otherUser} />
                ))}
              </> : ""
            }
          </ul>
        </div>
        {scopedMessageThread ?
          <div className="chat__thread-container">
            <ChatThread thread={scopedMessageThread} />
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

const ThreadAvailable = ({ threadId, otherUser }) => {
  const otherUserName = `${otherUser.firstName} ${otherUser.lastName}`;
  const otherUserThumbnail = `/f/profile_${otherUser.id}_64p.jpg`;
  const otherUserThumbAlt = `User ${otherUser.id} profile picture`;
  const threadUrl = `/messages/${threadId}`;
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
