import { useEffect, useRef, useState } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { useLocation, useParams } from "react-router-dom";

import * as chatActions from "../../store/reducers/chat"
import * as connectionsActions from "../../store/reducers/connections"
import * as sessionActions from "../../store/reducers/session"
import Typing from "../Chat/Typing";
import ImagePreload from "../ImagePreload/ImagePreload";

const ChatThread = ({ scrollToBottom }) => {
  // URL slug
  const { slug: hookSlug } = useParams();

  // Hooks
  const chat = useSelector(s => s.chat);
  const established = useSelector(s => s.connections.established);
  const notifications = useSelector(s => s.connections.notifications);
  const dispatch = useDispatch();

  // Component state
  const [slug, setSlug] = useState(null);
  const [chatPropagated, setChatPropagated] = useState(false);
  const [connection, setConnection] = useState(null);
  const [message, setMessage] = useState("");
  const [thread, setThread] = useState(null);
  const [composing, setComposing] = useState(false);
  const [joined, setJoined] = useState(false);

  // ******************************************************
  // because apparently useParams doesn't work as a
  // useEffect dependency get the slug to a local state var
  // on every render
  useEffect(() => {
    setSlug(hookSlug);
  }, [hookSlug]);

  // ******************************************************
  // side effect awaits Redux population of the chat object
  useEffect(() => {
    if (chat[slug]) setChatPropagated(true);
  }, [chat, slug]);

  // ******************************************************
  // side effect checks if the user is established connection
  useEffect(() => {
    if (slug && established[slug]) setConnection(established[slug]);
  }, [established, slug])

  // ******************************************************
  // side effect propagates aggregate chat feed and spoofs a
  // message thread for new connections threads by default
  useEffect(() => {
    if (connection) {
      if (chat[slug]) setThread(aggregateThread()(chat[slug]));
      else if (connection && connection.lastMessage) {
        dispatch(chatActions.getMessages({
          connId: slug,
          qty: 30,
          offsetQty: 0,
        }));
      }
      else {
        dispatch(connectionsActions.spoofMessageConnection(slug));
        dispatch(chatActions.spoofGetMessages(slug));
      }
    }
  }, [connection, slug, chat]);

  // ******************************************************
  // side effect handles peer room join and leave
  useEffect(() => {
    if (connection && !joined) {
      setJoined(true);
      const oid = connection.otherUser.id;
      dispatch(sessionActions.joinSocketClientRoom(oid));
      return () => dispatch(sessionActions.leaveSocketClientRoom(oid));
    }
  }, [connection, slug]);

  // ******************************************************
  // side effect clears all chat notifications for a thread
  // when the user is viewing the thread
  useEffect(() => {
    if (notifications.length) {
      dispatch(connectionsActions.clearChatNotification(slug));
    }
  }, [slug]);

  // ******************************************************
  // side effect removes connection notifications when the
  // slug is equal to the notification key
  useEffect(() => {
    const not = notifications[slug] ? notifications[slug] : null;
    if (not) dispatch(connectionsActions.clearChatNotification(slug))
  }, [chatPropagated, notifications, slug])

  // ******************************************************
  // side effect forces a scroll to bottom on propagation
  useEffect(() => {
    if (chatPropagated) scrollToBottom();
  }, [chatPropagated, thread])

  // ******************************************************
  // side effect emits composing state on message composition
  useEffect(() => {
    if (connection) {
      const oid = connection.otherUser.id;
      const cmp = composing;
      const msg = message.length;
      const cid = parseInt(slug);
      if (msg && !cmp) {
        setComposing(true);
        dispatch(chatActions.postComposerInteracting(oid, cid));
      }
      else if (!msg && cmp) {
        setComposing(false);
        dispatch(chatActions.deleteComposerInteracting(oid, cid))
      }
    }
  }, [composing, message, connection])

  // ******************************************************
  // event listener expects an enter keystroke to submit the
  // message form and then clear the message input
  const onMessageKeyDown = (evt) => {
    if (evt.key === "Enter" || evt.keyCode === 13) {
      evt.preventDefault();
      dispatch(chatActions.postMessage({
        connId: parseInt(slug),
        body: message,
      }));
      setMessage("");
    }
  }

  // ******************************************************
  // event listener updates message value
  const onMessageChange = (evt) => {
    const val = evt.target.value;
    setMessage(val);
  }

  return (
    <>
      {chatPropagated ?
        <>
          <div className="chat-thread">
            <div className="messages">
              {thread}
            </div>
          </div>
          <div className="compose page-grid">
            <textarea
              value={message}
              onChange={onMessageChange}
              onKeyDown={onMessageKeyDown}
              placeholder="Write your message here..." />
            <div className="typing">
            </div>
          </div>
        </> : ""
      }
    </>
  );
}

// closure function receives a chat Notifications and aggregates
const aggregateThread = () => {
  // tracks message days to prevent duplicate markers
  // several sources of.notificationsmaterial into a single thread
  const dateMarkerMemo = [];
  // holds a sorted collection of thread components
  const components = [];
  // closure function collects disparate items into an array
  // for processing into a message thread
  return (chatContext) => {
    const aggregate = [...chatContext.messages];
    aggregate.forEach((x, i) => {
      const dateString = new Date(x.createdAt).toDateString();
      if (!dateMarkerMemo.includes(dateString)) {
        components.push(<DateMarker key={`thread-aggr-mrk-${i}`} date={x.createdAt} />);
        dateMarkerMemo.push(dateString);
      }
      if (x.aggrType === "message") {
        components.push(<MessageBubble key={`thread-aggr-msg-${i}`} message={x} />);
      }
    });
    return components;
  }
}

const DateMarker = ({ date }) => {
  // Convert date to user-friendly format
  let dateString = "";
  const todaysDate = new Date();
  const markerDate = new Date(date);

  const todaysWeekDay = todaysDate.getDay();
  const todaysMonthDay = todaysDate.getDate();
  const todaysMonth = todaysDate.getMonth();
  const todaysYear = todaysDate.getFullYear();
  const markerWeekDay = markerDate.getDay();
  const markerMonthDay = markerDate.getDate();
  const markerMonth = markerDate.getMonth();
  const markerYear = markerDate.getFullYear();

  const todaysWeekStartDay = todaysMonthDay - todaysWeekDay;

  const weekDayConvert = (dayInt) => {
    switch (dayInt) {
      case 0: return "Sunday"
      case 1: return "Monday"
      case 2: return "Tuesday"
      case 3: return "Wednesday"
      case 4: return "Thursday"
      case 5: return "Friday"
      case 6: return "Saturday"
      default: RangeError("dayInt must be between 0 and 6 inclusive.");
    }
  }
  const monthConvert = (monthInt) => {
    switch (monthInt) {
      case 0: return "January"
      case 1: return "February"
      case 2: return "March"
      case 3: return "April"
      case 4: return "May"
      case 5: return "June"
      case 6: return "July"
      case 7: return "August"
      case 8: return "September"
      case 9: return "October"
      case 10: return "November"
      case 11: return "December"
      default: RangeError("monthInt must be between 0 and 11 inclusive.");
    }
  }

  if (todaysYear > markerYear) {
    dateString = `${monthConvert(markerMonth)} ${markerMonthDay}, ${markerYear}`;
  }
  else if (todaysMonth >= markerMonth && markerMonthDay < todaysWeekStartDay) {
    dateString = `${monthConvert(markerMonth)} ${markerMonthDay}`;
  }
  else if (markerWeekDay !== todaysWeekDay) {
    dateString = weekDayConvert(markerWeekDay);
  }
  else {
    dateString = "Today";
  }

  return (
    <h2 className="date">{dateString}</h2>
  );
}

const MessageBubble = ({ message }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);

  // Component state
  const [timeSent, setTimeSent] = useState("");
  const whose = message.sender.id === sessionUser.id ? "mine" : "theirs";
  const imageSrc = `/f/profile_${message.sender.id}_64p.jpg`;

  useEffect(() => {
    setTimeSent(updateTimeSent(message));
    const bubbleUpdateInterval = setInterval(() => {
      setTimeSent(updateTimeSent(message));
    }, 10000);
    return () => clearInterval(bubbleUpdateInterval);
  });

  // Returns a string articulating the time of the sent message
  const updateTimeSent = (message) => {
    const todDate = new Date();
    const todDateStr = todDate.toDateString();
    const msgDate = new Date(message.createdAt);
    const msgDateStr = msgDate.toDateString();

    const todHr = todDate.getHours();
    const todMin = todDate.getMinutes();
    const msgHr = msgDate.getHours();
    const msgMin = msgDate.getMinutes();
    let adjMsgHr = msgHr;
    let amPm = "AM";
    let out = "";

    if (msgHr > 12) {
      amPm = "PM";
      adjMsgHr -= 12;
    }
    else if (msgHr === 12) {
      amPm = "PM";
    }
    if (todDateStr === msgDateStr && msgMin === todMin) {
      out = "Less than a minute ago";
    }
    else if (todDateStr === msgDateStr && todHr === msgHr) {
      const mins = todMin - msgMin;
      if (mins === 1) out = "A minute ago";
      else out = `${mins} minutes ago`;
    }
    else {
      out = `${adjMsgHr}:${msgMin} ${amPm}`;
    }

    return out;
  }

  return (
    <div className={"bubble " + whose}>
      <ImagePreload src={imageSrc} />
      <div className="white-space">
        <p className="body">{message.body}</p>
        <p className="sent">{timeSent}</p>
      </div>
    </div>
  )
}

export default ChatThread;
