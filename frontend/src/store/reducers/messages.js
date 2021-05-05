import { MessageManager } from "../models/message";
import { fetch } from "../utilities/fetch";
import { requires, socket } from "../index";

const messagesManager = new MessageManager();

const LIMIT = 5;

// const POST_MESSAGE = "messages ——————————> POST_MESSAGE"
const GET_MESSAGES = "messages ——————————> GET_MESSAGES";
// const UPDATE_MESSAGE = "messages ——————————> UPDATE_MESSAGE"
// const DELETE_MESSAGE = "messages ——————————> DELETE_MESSAGE"
// const COMPOSE_MESSAGE = "messages ——————————> COMPOSE_MESSAGE"
// const ABANDON_MESSAGE = "messages ——————————> ABANDON_MESSAGE"

export const getMessages = ({ connectionId }) => async (dispatch) => {
  requires.session();
  socket.require();

  const collection = messagesManager.syncCollectionOffset(connectionId, LIMIT); // prettier-ignore
  const offset = collection ? collection.offset : 0;
  
  const query = `?ofs=${offset}&lim=${LIMIT}`;

  const endpoint = messagesManager.endpoint + `/${connectionId}/messages${query}`;
  const { data } = await fetch(endpoint, { method: "GET" });

  dispatch(getMessagesAction(data));
};

const getMessagesAction = (payload) => ({type: GET_MESSAGES, payload });

const reducer = (state = messagesManager.state(), { type, payload }) => {
  switch (type) {
    case GET_MESSAGES:
      messagesManager.populateCollection(payload);
      return messagesManager.state();

    default:
      return state;
  }
};

export default reducer;
