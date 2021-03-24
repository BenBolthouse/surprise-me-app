import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";

import * as chatActions from "../../store/reducers/chat"
import * as connectionsActions from "../../store/reducers/connections"
import * as sessionActions from "../../store/reducers/session"
import Typing from "../Chat/Typing";
import ImagePreload from "../ImagePreload/ImagePreload";

const ChatThread = () => {
  // URL slug
  const { slug } = useParams();

  // Ref for scroll layer
  const scrollLayerRef = useRef(null);

  // Hooks
  const chat = useSelector(s => s.chat);
  const connections = useSelector(s => s.connections);
  const sessionUser = useSelector(s => s.session.user);
  const sessionSocketClient = useSelector(s => s.session.socketClient);
  const connectionsNotifications = useSelector(s => s.connections.notifications);
  const dispatch = useDispatch();

  // Component state
  const [message, setMessage] = useState("");
  const [thread, setThread] = useState(null);
  const [isScrolledToBottom, setIsScrolledToBottom] = useState(true);
  
  // side effect awaits loading of messages and then
  // triggers a change in component state to allow
  // conditional render
  useEffect(() => {
    // check if the user is connected to the other user
    if (connections.established[slug]) {
      // then do the magic
      if (chat[slug]) {
        setThread(aggregateThread()(chat[slug]));
      }
      else if (connections.established[slug].lastMessage) {
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
  }, [slug, chat, connections]);

  useEffect(() => {
    const otherUserId = connections.established[slug].otherUser.id;
    dispatch(sessionActions.joinSocketClientRoom(otherUserId));
    return () => {
      dispatch(sessionActions.leaveSocketClientRoom(otherUserId));
    }
  }, [sessionSocketClient, slug])

  useEffect(() => {
    if (connectionsNotifications.length) {
      dispatch(connectionsActions.clearChatNotifications(slug));
    }
  }, [slug]);

  // event listener expects an enter keystroke to submit the
  // message form and then clear the message input
  const onSubmit = (evt) => {
    if (evt.key === "Enter" || evt.keyCode === 13) {
      evt.preventDefault();
      dispatch(chatActions.postMessage({
        connId: parseInt(slug),
        body: message,
      }));
      setMessage("");
    }
  }




  const onScroll = (evt) => {
    const current = scrollLayerRef.current;
    const currentScroll = current.scrollTop + current.clientHeight;
    const threshold = (current.scrollHeight - currentScroll) < 300
      ? true
      : false;
    if (threshold && !isScrolledToBottom) {
      setIsScrolledToBottom(true)
    }
    else if (!threshold && isScrolledToBottom) {
      setIsScrolledToBottom(false)
    }
  }

  return (
    <>
      {thread ?
        <div
          onScroll={onScroll}
          ref={scrollLayerRef}
          className="scroll">
          <div className="chat-thread">
            <div className="messages">
              {thread}
            </div>
          </div>
          <div className="compose page-grid">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={onSubmit}
              placeholder="Write your message here..." />
            <div className="typing">
            </div>
          </div>
        </div> : ""
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
      <h3>{message.sender.firstName}</h3>
      <p className="body">{message.body}</p>
      <p className="sent">{timeSent}</p>
    </div>
  )
}

export default ChatThread;
