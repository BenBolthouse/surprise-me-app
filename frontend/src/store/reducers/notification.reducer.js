import notificationsManager from "../models/notifications.model";

export const addNotification = (props) => {
  const payload = notificationsManager
    .collection(props.type)
    .createEntity({ ...props, id: _getId() })
    .setCreatedAt();

  return { type: "notifications/ADD_NOTIFICATION —> " + props.type, payload };
};

export const seeNotification = (props) => {
  const payload = notificationsManager
    .collection(props.type)
    .entity((x) => x.id === props.id)
    .setSeenAt();

  return { type: "notifications/SEE_NOTIFICATION —> " + props.type, payload };
};

export const dismissNotification = (props) => {
  const payload = notificationsManager
    .collection(props.type)
    .entity((x) => x.id === props.id)
    .setSeenAt()
    .setDismissedAt();

  return { type: "notifications/DISMISS_NOTIFICATION —> " + props.type, payload };
};

const reducer = (state = notificationsManager.return(), { type }) => {
  switch (type) {
    default:
      return state;
  }
};

let _idSequence = 1;

const _getId = () => _idSequence++;

export default reducer;
