import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { NavLink, useParams } from "react-router-dom";
import { BsArrowLeftShort } from "react-icons/bs";

import ChatThread from "../ChatThread/ChatThread";

import * as sessionActions from "../../store/reducers/session";

import "./Chat.css";
import ImagePreload from "../ImagePreload/ImagePreload";

const Chat = () => {
  // URL slug
  const { slug } = useParams()

  // Hooks
  const connections = useSelector(s => s.connections);
  const dispatch = useDispatch();

  // Component state
  const [activeMessageThreads, setActiveMessageThreads] = useState(null);

  // side effect gets the users with chat history to a
  // collection for recent chats and joins the user chat
  // rooms
  useEffect(() => {
    const messageThreads = [];
    for (const value of Object.values(connections.established)) {
      if (value.lastMessage) {
        messageThreads.push(value)
      };
    }
    setActiveMessageThreads(messageThreads);
  }, [connections]);

  return (
    <div className="chat-viewport-container">
      <div className="view chat-view page-grid">
        <div className="chat__mobile-nav">
          <NavLink activeClassName="hide" to="/messages/start">
            <BsArrowLeftShort />
          </NavLink>
          <input
            type="text"
            name="search-mobile"
            id="chatRecentsSearchMobile"
            placeholder="Search" />
        </div>
        <div className="chat__recent-threads">
          <div>
            <div className="search">
              <input
                type="text"
                name="search"
                id="chatRecentsSearch"
                placeholder="Search" />
            </div>
            <h2>Recents</h2>
            <div className="scroll">
              <ul>
                {activeMessageThreads
                  ? activeMessageThreads.map((messageThread) => (
                    <ThreadAvailable
                      imageSize="64"
                      key={`active-message-thread-${messageThread.id}`}
                      thread={messageThread}
                    />
                  ))
                  : ""}
              </ul>
            </div>
          </div>
        </div>
        <div className="chat__content">
          {slug !== "start" ?
            <div>
              {slug ? <ChatThread /> : ""}
            </div> :
            <>
              <div className="chat__splash">
                <div>
                  <h1>Messages</h1>
                  <p>Select or search for a friend to start a conversation.</p>
                </div>
              </div>
              <div className="chat__splash-mobile">
                <h2>Recents</h2>
                <div className="scroll">
                  <ul>
                    {activeMessageThreads
                      ? activeMessageThreads.map((messageThread) => (
                        <ThreadAvailable
                          imageSize="128"
                          key={`active-message-thread-${messageThread.id}`}
                          thread={messageThread}
                        />
                      ))
                      : ""}
                  </ul>
                </div>
              </div>
            </>
          }
        </div>
      </div>
    </div>
  );
}

const ThreadAvailable = ({ thread, imageSize }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);
  const chatThread = useSelector(s => s.chat[thread.id]);
  const connectionsNotifications = useSelector(s => s.connections.notifications);

  // Component state
  const [lastMessage, setLastMessage] = useState("")
  const [hasUnread, setHasUnread] = useState(false);
  const otherUserName = `${thread.otherUser.firstName} ${thread.otherUser.lastName}`;
  const otherUserThumbnail = `/f/profile_${thread.otherUser.id}_${imageSize}p.jpg`;
  const threadUrl = `/messages/${thread.id}`;

  useEffect(() => {
    let message = "";
    if (chatThread && chatThread.lastMessage) {
      message = chatThread.lastMessage;
    }
    else {
      message = thread.lastMessage;
    }
    if (message.sender.id === sessionUser.id) {
      setLastMessage("Me: " + message.body);
    }
    else {
      setLastMessage(message.body);
    }
  }, [chatThread]);

  useEffect(() => {
    if (connectionsNotifications.find(
      n => n.userConnectionId === thread.id
    )) {
      setHasUnread(true);
    }
    else setHasUnread(false);
  }, [connectionsNotifications])

  return (
    <NavLink to={threadUrl}>
      <li>
        <ImagePreload src={otherUserThumbnail} />
        <p className="name">{otherUserName}</p>
        <p className="last-message">{lastMessage}</p>
        {hasUnread ?
          <div className="unread" /> : ""
        }
      </li>
    </NavLink>
  );
}

export default Chat;
