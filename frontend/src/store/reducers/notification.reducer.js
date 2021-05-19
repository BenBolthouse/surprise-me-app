/** @ignore */
const model = {
  bell: [],
  card: [],
  message: [],
  popup: [],
};

/** @ignore */
const hex = () => {
  let output = "";
  const chars = "ABCDEF0123456789";
  for (let i = 0; i < 7; i++) {
    const idx = Math.floor(Math.random() * chars.length);
    output += chars[idx];
  }
  return output;
};

const reducer = (state = model, { type, payload }) => {
  const stateCopy = { ...state };

  switch (type) {
    /** */
    case "notifications/GET":
      stateCopy.bell = payload.filter(x => x.type === "bell");
      stateCopy.message = payload.filter(x => x.type === "message");
      return stateCopy;

    case "notifications/bell/POST":
      stateCopy.bell.push(payload);
      return stateCopy;

    case "notifications/bell/DISMISS":
      payload.forEach((id) => {
        stateCopy.bell.find((x) => x.id === id).dismissedAt = new Date();
      });
      return stateCopy;

    case "notifications/card/CREATE":
      payload.id = hex();
      stateCopy.card.push(payload);
      return stateCopy;

    case "notifications/card/DISMISS":
      stateCopy.card.find((x) => x.id === payload).dismissedAt = new Date();
      return stateCopy;

    case "notifications/message/POST":
      stateCopy.message.push(payload);
      return stateCopy;

    case "notifications/message/DISMISS":
      payload.forEach((id) => {
        stateCopy.message.find((x) => x.id === id).dismissedAt = new Date();
      });
      return stateCopy;

    case "notifications/popup/CREATE":
      stateCopy.popup.push(payload);
      return stateCopy;

    default:
      return state;
  }
};

export default reducer;
