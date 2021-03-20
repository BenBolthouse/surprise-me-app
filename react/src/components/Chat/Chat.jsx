import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { NavLink } from "react-router-dom";
import { IoMdMailUnread } from "react-icons/io";

import "./Chat.css";

const Chat = ({ children }) => {

  // Hooks
  const connections = useSelector(s => s.connections);
  const estConnections = useSelector(s => s.connections.established);
  const notifications = useSelector(s => s.notifications);

  // Component state
  const [threadsAvail, setThreadsAvail] = useState(false);
  const [mount, setMount] = useState(false);

  // Side effect for mount component
  useEffect(() => {
    // Get all existing chat threads
    const threads = []
    for (const [key, value] of Object.entries(estConnections)) {
      if (value.hasChatHistory) threads.push(value);
    }
    setThreadsAvail(threads);

    setMount(true);
  }, []);

  return (
    <>
      {mount ?
        <div className="chat-viewport-container">
          <div className="view chat-view">
            <div className="chat__sidebar">
              <ul className="chat__threads-available">
                {threadsAvail.map(thread => (
                  <ThreadAvailable
                    threadId={thread.id}
                    otherUser={thread.otherUser} />
                ))}
              </ul>
            </div>
          </div>
        </div> : ""
      }
    </>
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
