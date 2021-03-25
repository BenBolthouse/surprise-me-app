import _ from "lodash";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";

import ImagePreload from "../ImagePreload/ImagePreload";
import Typing from "./Typing";

const RecentThread = ({ thread: chatThread, imageSize }) => {
  // URL slug
  const { slug: hookSlug } = useParams();

  // locals
  const { id, otherUser } = chatThread;

  // Hooks
  const notifications = useSelector(s => s.connections.notifications);
  const sessionUser = useSelector(s => s.session.user);
  const connections = useSelector(s => s.connections);
  const chat = useSelector(s => s.chat);

  // Component state
  const [slug, setSlug] = useState(null);
  const [lastMessage, setLastMessage] = useState("")
  const [connection, setConnection] = useState(null);
  const [thread, setThread] = useState(null);
  const [unread, setUnread] = useState(false);
  const [composing, setComposing] = useState(false);

  // ******************************************************
  // because apparently useParams doesn't work as a
  // useEffect dependency get the slug to a local state var
  // on every render
  useEffect(() => {
    setSlug(hookSlug);
  }, [hookSlug]);

  // ******************************************************
  // side effect gets the messages from chat for this thread
  useEffect(() => {
    if (chat[chatThread.id] && !thread) setThread(chat[chatThread.id]);
  }, [chat, thread]);

  // ******************************************************
  // side effect checks if the user is established connection
  useEffect(() => {
    const est = connections.established;
    if (est[id] && !connection) setConnection(est[id]);
  }, [connections])

  // ******************************************************
  // side effect gets the last message in the thread
  useEffect(() => {
    let msg;
    const sid = sessionUser.id;
    const cht = chat[id] ? chat[id] : null;
    const con = connection ? connection : null;
    if (cht && cht.lastMessage) msg = cht.lastMessage;
    else if (con && con.lastMessage) msg = con.lastMessage;
    if (msg && msg.sender.id === sid) setLastMessage(`Me: ${msg.body}`);
    else if (msg) setLastMessage(msg.body);
  }, [connections, connection, chat])

  // ******************************************************
  // side effect sets the unread bulb if notifications change
  useEffect(() => {
    if (!_.isEmpty(notifications[id])) setUnread(true);
  }, [notifications, id])

  // ******************************************************
  // side effect clears the notification bulb if user on thread
  useEffect(() => {
    if (parseInt(slug) === id) setUnread(false);
  }, [slug, id])

  // ******************************************************
  // side effect detects if other user is composing
  useEffect(() => {
    const cht = chat[id];
    if (cht && cht.interacting) {
      setComposing(true);
    }
    else setComposing(false);
  }, [chat])

  return (
    <NavLink to={`/messages/${id}`}>
      <li>
        <ImagePreload src={`/f/profile_${otherUser.id}_${imageSize}p.jpg`} />
        <p className="name">{otherUser.firstName} {otherUser.lastName}</p>
        <p className="last-message">{composing ?
          <Typing usersName={otherUser.firstName} /> : lastMessage
        }</p>
        <div className={`unread ${unread ? "show" : "hide"}`} />
      </li>
    </NavLink>
  );
}

export default RecentThread;
