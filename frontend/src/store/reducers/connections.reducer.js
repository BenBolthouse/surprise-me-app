/** @ignore */
const model = {
  requested: [],
  pending: [],
  approved: [],
};

const moveToCollection = (id, source, destination) => {
  const item = source.find(x => x.id === id);
  const index = source.indexOf(item);

  source.splice(index, 1);

  destination.push(item);
};

const removeFromCollections = (id, ...sources) => {
  sources.forEach((source) => {
    const item = source.find((x) => x.id === id);
    const index = source.indexOf(item);

    source.splice(index, 1);
  });
};

const reducer = (state = model, { type, payload }) => {
  const stateCopy = { ...state };

  switch (type) {
    case "connections/POST":
      stateCopy.requested.push(payload);
      return stateCopy;

    case "connections/GET":
      stateCopy.requested = payload.connections.filter((x) => {
        const a = x.requestorId === payload.userId;
        const b = x.approvedAt === null;
        return a && b;
      });
      stateCopy.pending = payload.connections.filter((x) => {
        const a = x.requestorId !== payload.userId;
        const b = x.approvedAt === null;
        return a && b;
      });
      stateCopy.approved = payload.connections.filter(
        (x) => x.approvedAt !== null
      );
      return stateCopy;

    case "connections/APPROVE":
      moveToCollection(payload.id, stateCopy.pending, stateCopy.approved);
      return stateCopy;

    case "connections/DENY":
      removeFromCollections(
        stateCopy.requested,
        stateCopy.pending,
        stateCopy.approved
      );
      return stateCopy;

    case "connections/LEAVE":
      removeFromCollections(
        stateCopy.requested,
        stateCopy.pending,
        stateCopy.approved
      );
      return stateCopy;

    default:
      return state;
  }
};

export default reducer;
