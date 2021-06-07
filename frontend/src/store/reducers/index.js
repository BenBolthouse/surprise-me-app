import { connectionsReducer } from "./reducer.connections";
import { notificationsReducer } from "./reducer.notifications";
import { sessionReducer } from "./reducer.session";
import { userReducer } from "./reducer.user";

export default {
  connections: connectionsReducer,
  notifications: notificationsReducer,
  session: sessionReducer,
  user: userReducer,
};
