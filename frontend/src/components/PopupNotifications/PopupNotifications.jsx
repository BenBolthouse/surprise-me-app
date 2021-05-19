/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";

import "./popup_notifications.css";

const PopupNotifications = ({ children }) => {
  const notifications = useSelector(x => x.notifications.popup);

  const [notification, setNotification] = useState(null);
  const [hideNotification, setHideNotification] = useState(false);

  useEffect(() => {
    if (notifications.length) {
      setNotification(notifications[notifications.length - 1]);
      setHideNotification(false);
    }
  }, [notifications.length]);

  useEffect(() => {
    let timeout;

    if (notification) {
      timeout = setTimeout(() =>
        setHideNotification(true),
        notification.duration * 1000 || 3000)
    }

    return () => clearTimeout(timeout);
  }, [notification]);

  const notificationImportanceClass = notification && notification.importance
    ? ` ${notification.importance}`
    : " gray";
  const notificationHideClass = hideNotification ? " hide" : " show";

  const notificationClasses = "notification" +
    notificationImportanceClass +
    notificationHideClass;

  return (
    <>
      <div className="view popup-notifications-view">
        <div className="container">
          {!notification ? null :
            <div className={notificationClasses}>
              <span>{notification.body}</span>
            </div>
          }
        </div>
      </div>
      { children}
    </>
  )
}

export default PopupNotifications;
