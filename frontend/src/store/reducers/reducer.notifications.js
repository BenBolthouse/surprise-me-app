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

export const notificationsReducer = (state = model, { type, payload }) => {
  const stateCopy = { ...state };
  const data = payload ? payload.data : null;

  switch (type) {
    case "notifications/GET":
      stateCopy.bell = data.filter((x) => x.type === "bell");
      stateCopy.message = data.filter((x) => x.type === "message");
      return stateCopy;

    case "notifications/bell/POST":
      stateCopy.bell.push(data);
      return stateCopy;

    case "notifications/bell/DISMISS":
      data.forEach((id) => {
        stateCopy.bell.find((x) => x.id === id).dismissedAt = new Date();
      });
      return stateCopy;

    case "notifications/card/CREATE":
      data.id = hex();
      stateCopy.card.push(data);
      return stateCopy;

    case "notifications/card/DISMISS":
      stateCopy.card.find((x) => x.id === data).dismissedAt = new Date();
      return stateCopy;

    case "notifications/message/POST":
      stateCopy.message.push(data);
      return stateCopy;

    case "notifications/message/DISMISS":
      data.forEach((id) => {
        stateCopy.message.find((x) => x.id === id).dismissedAt = new Date();
      });
      return stateCopy;

    case "notifications/popup/CREATE":
      console.log(payload);
      stateCopy.popup.push(data);
      return stateCopy;

    default:
      return state;
  }
};
