import { Collection, EntityBase, Manager } from "../entity";

class Notification extends EntityBase {
  constructor() {
    super(
      {
        type: "String",
        body: "String",
        actionLabel: "String",
        action: "String",
        delay: "Number",
        seenAt: "Date",
        dismissedAt: "Date",
      },
      { randomHashId: true, randomHashLength: 8 }
    );
  }

  setSeenAt() {
    this.seenAt = new Date();

    return this;
  }

  setDismissedAt() {
    this.dismissedAt = new Date();

    return this;
  }
}

const uiNotificationsCollection = new Collection({
  name: "card_notifications",
  model: Notification,
});

const popupNotificationsCollection = new Collection({
  name: "popup_notifications",
  model: Notification,
});

const bellNotificationsCollection = new Collection({
  syncToLocalStorage: true,
  name: "bell_notifications",
  model: Notification,
});

const messageNotificationsCollection = new Collection({
  syncToLocalStorage: true,
  name: "message_notifications",
  model: Notification,
});

const notificationsManager = new Manager({
  uiNotificationsCollection,
  popupNotificationsCollection,
  bellNotificationsCollection,
  messageNotificationsCollection,
});

export default notificationsManager;
