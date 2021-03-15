import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { NavLink } from "react-router-dom";
import { IconContext, IoMdMailUnread } from "react-icons/io";

import "./Chat.css";

const Chat = ({ children }) => {

  // Hooks
  const connections = useSelector(s => s.connections);
  const notifications = useSelector(s => s.notifications);

  // Component state
  const [mount, setMount] = useState(false);
  const [activeChats, setActiveChats] = useState([])

  // Side effect get a list of all active chats on
  // notifications or connections changes.
  useEffect(() => {
    if (connections.datestamp && notifications.datestamp) {
      // Get only the connections with messages to an active
      // chats array
      const active = [];
      const established = connections.established;
      for (const i in established) {
        if (established[i].messages.length) {
          if (notifications.chat[i]) {
            active.push({
              ...established[i],
              messages: null,
              read: "unread",
            })
          }
          else {
            active.push({
              ...established[i],
              messages: null,
              read: "read",
            })
          }
        }
      }
      setActiveChats(active);
      setMount(true);
    };
  }, [connections, notifications])

  return (
    <>
      {mount ?
        <div className="view chat-view">
          <div className="chat__sidebar">
            <ul className="chat__threads-available">
              {activeChats.map(persona => (
                <NavLink
                  activeClassName="active"
                  key={`chat-persona-${persona.id}`}
                  to={`/messages/${persona.connectionId}`}>
                  <li className={`chat__on-${persona.read}`}>
                    <img alt="Profile picture" src={`/f/profile_${persona.connectionUserId}_64p.jpg`} />
                    <p>{`${persona.connectionFirstName} ${persona.connectionLastName}`}</p>
                    <div className="unread-icon">
                      <IoMdMailUnread color="#f2075a" />
                    </div>
                  </li>
                </NavLink>
              ))}
            </ul>
          </div>
          <div className="chat__thread-container">
            {children}
          </div>
        </div> : ""
      }
    </>
  );
}

export default Chat;
