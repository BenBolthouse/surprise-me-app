import _ from "lodash";

import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

const Chat = ({ children }) => {

  // Hooks
  const sessionUser = useSelector(s => s.session.user);
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
      const estConnections = connections.established.connections;
      for (const i in estConnections) {
        if (estConnections[i].messages.length) {
          if (notifications.chat[i]) {
            active.push({
              ...estConnections[i],
              messages: null,
              read: "unread",
            })
          }
          else {
            active.push({
              ...estConnections[i],
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
        <div className="chat">
          <div className="chat__sidebar">
            <ul className="chat__threads-available">
              {activeChats.map(persona => (
                <Link
                  key={`chat-persona-${persona.id}`}
                  to={`/messages/${persona.connectionId}`}>
                  <li className={`chat__persona-on-${persona.read}`}>
                    <p>{`${persona.connectionFirstName} ${persona.connectionLastName}`}</p>
                  </li>
                </Link>
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
