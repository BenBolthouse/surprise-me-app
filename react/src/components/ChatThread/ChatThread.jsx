import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";

import * as chatActions from "../../store/reducers/chat"
import * as sessionActions from "../../store/reducers/session"

const ChatThread = () => {
  // URL slug
  const { slug } = useParams();

  // Ref for scroll layer
  const scrollLayerRef = useRef(null);

  // Hooks
  const chat = useSelector(s => s.chat);
  const connections = useSelector(s => s.connections);
  const sessionSocketClient = useSelector(s => s.session.socketClient);
  const dispatch = useDispatch();

  // Component state
  const [message, setMessage] = useState("");
  const [mount, setMount] = useState(false);
  const [thread, setThread] = useState(null);
  const [messages, setMessages] = useState(null);
  const [prevRoom, setPrevRoom] = useState(null);
  const [myInteract, setMyInteract] = useState(false);
  const [theirInteract, setTheirInteract] = useState(false);
  const [isScrolledToBottom, setIsScrolledToBottom] = useState(true);

  useEffect(() => {
    if (!chat[slug]) {
      dispatch(chatActions.getMessages({
        connId: slug,
        qty: 30,
        offsetQty: 0,
      }));
    }
    dispatch(sessionActions.joinSocketClientRoom(parseInt(slug)));
    if (prevRoom) dispatch(sessionActions.leaveSocketClientRoom(prevRoom));
  }, [slug]);

  useEffect(() => {
    if (chat[slug]) {
      setThread(connections.established[slug]);
      setTheirInteract(chat[slug].interacting);
      setPrevRoom(parseInt(slug));
      const agg = aggregateMessages();
      const messagesResult = agg(chat[slug].messages);
      setMessages(messagesResult);
    }
  }, [slug, chat]);

  useEffect(() => {
    if (scrollLayerRef.current && isScrolledToBottom) {
      scrollLayerRef.current.scrollTop = 1000000;
    }
  }, [messages]);

  useEffect(() => {
    if (mount) {
      if (message.length && !myInteract) {
        sessionSocketClient.emit("composer_interacting", {
          roomId: parseInt(slug),
          interacting: true,
        });
        setMyInteract(true);
      }
      else if (!message.length && myInteract) {
        sessionSocketClient.emit("composer_interacting", {
          roomId: parseInt(slug),
          interacting: false,
        });
        setMyInteract(false);
      }
    }
    else setMount(true);
  }, [message])

  // Event handlers
  const onTextAreaKeyDown = (evt) => {
    if (evt.key === "Enter" || evt.keyCode === 13) {
      evt.preventDefault();
      dispatch(chatActions.postMessage({
        connId: thread.id,
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
      {thread && messages ?
        <div
          onScroll={onScroll}
          ref={scrollLayerRef}
          className="scroll-layer">
          <div className="chat-thread">
            <div className="chat-thread__messages">
              {messages}
            </div>
          </div>
          <div className="compose-message">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={onTextAreaKeyDown}
              placeholder="Write your message here..." />
            <div className="chat-thread__typing">
              {theirInteract ?
                <>{thread.otherUser.firstName} is typing...</> : ""
              }
            </div>
          </div>
        </div> : ""
      }
    </>
  );
}

const aggregateMessages = () => {
  const dateMarkerMemo = [];
  const components = [];
  return (messages) => {
    messages.forEach((msg, i) => {
      const datestring = new Date(msg.createdAt).toDateString();
      if (!dateMarkerMemo.includes(datestring)) {
        components.push(<DateMarker key={`feed-aggr-date-${i}`} date={msg.createdAt} />);
        dateMarkerMemo.push(datestring);
      }
      components.push(<MessageBubble key={`feed-aggr-msg-${i}`} message={msg} />);
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
      case 1: return "January"
      case 2: return "February"
      case 3: return "March"
      case 4: return "April"
      case 5: return "May"
      case 6: return "June"
      case 7: return "July"
      case 8: return "August"
      case 9: return "September"
      case 10: return "October"
      case 11: return "November"
      case 12: return "December"
      default: RangeError("monthInt must be between 1 and 12 inclusive.");
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
    <h2 className="chat-thread__date-marker">{dateString}</h2>
  );
}

const MessageBubble = ({ message }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);

  // Component state
  const [timeSent, setTimeSent] = useState("");
  const whose = message.sender.id === sessionUser.id ? "mine" : "theirs";

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
    <div className={"message-bubble " + whose}>
      <h3>{message.sender.firstName}</h3>
      <p className="message-bubble__body">{message.body}</p>
      <p className="message-bubble__time">{timeSent}</p>
    </div>
  )
}

export default ChatThread;
