import { NavLink, useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { useSelector } from "react-redux";

import { BsList as BackIcon } from "react-icons/bs";
import { BsSearch as SearchIcon } from "react-icons/bs";

import ChatThread from "../ChatThread/ChatThread";

import "./Chat.css";
import RecentThread from "./RecentThread";
import Search from "../Search/Search";
import ChatSearchItem from "./ChatSearchItem";

const Chat = () => {
  // URL slug
  const { slug: hookSlug } = useParams()

  // references the main scrollable content area
  const scrollRef = useRef(null);

  // Hooks
  const established = useSelector(s => s.connections.established);

  // Component state
  const [slug, setSlug] = useState(null);
  const [recents, setRecents] = useState(null);
  const [search, setSearch] = useState(false);

  // ******************************************************
  // because apparently useParams doesn't work as a
  // useEffect dependency get the slug to a local state var
  // on every render
  useEffect(() => {
    setSlug(hookSlug);
  }, [hookSlug]);

  // ******************************************************
  // side effect gets the users with chat history to a
  // collection for recent chats and joins the user chat
  // rooms
  useEffect(() => {
    const est = established;
    const thr = [];
    for (const val of Object.values(est)) {
      if (val.lastMessage) thr.push(val)
    }
    setRecents(thr);
  }, [established, slug]);

  // ******************************************************
  // event handler detects scroll events in the content area
  const onContentScroll = (evt) => {
    const current = scrollRef.current;
    const scrollTop = current.scrollTop;
    const scrollHeight = current.scrollHeight;
    const clientHeight = current.clientHeight;
  }

  // ******************************************************
  // event handler detects focus events in the search bar
  const onSearchFocus = (evt) => setSearch(true);

  // ******************************************************
  // helper function returns the user to the bottom of the thread
  const scrollToBottom = () => {
    const current = scrollRef.current;
    const scrollTop = current.scrollTop;
    const scrollHeight = current.scrollHeight;
    const clientHeight = current.clientHeight;
    scrollRef.current.scrollTop = scrollHeight;
  }

  return (
    <div className="chat-viewport-container">
      <div className="view chat-view page-grid">
        {search ?
          <Search
            filter="connections"
            prompt="Start typing to search for friends..."
            ItemComponent={ChatSearchItem}
            obscurityCallback={() => setSearch(false)} /> : null
        }
        <div className="chat__mobile-nav">
          <NavLink activeClassName="hide" to="/messages/start">
            <BackIcon className="hamburger-icon"/>
          </NavLink>
          <h1>Messages</h1>
          <SearchIcon
            className="search-icon"
            onClick={() => setSearch(true)} />
        </div>
        <div className="chat__recent-threads">
          <div>
            <div className="search-spoof">
              <input
                type="text"
                name="search"
                id="chatRecentsSearch"
                onFocus={onSearchFocus}
                placeholder="Search" />
            </div>
            <h2>Recents</h2>
            <div className="scroll">
              <ul>
                {recents
                  ? recents.map((messageThread) => (
                    <RecentThread
                      imageSize="64"
                      thread={messageThread}
                      key={`active-message-thread-${messageThread.id}`} />
                  ))
                  : ""}
              </ul>
            </div>
          </div>
        </div>
        <div
          className="chat__content"
          ref={scrollRef}
          onScroll={onContentScroll}>
          {slug !== "start" ?
            <div>
              <div className="scroll">
                {slug ?
                  <ChatThread scrollToBottom={scrollToBottom} /> : ""
                }
              </div>
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
                    {recents
                      ? recents.map((messageThread) => (
                        <RecentThread
                          imageSize="128"
                          thread={messageThread}
                          key={`active-message-thread-m-${messageThread.id}`} />
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

export default Chat;
