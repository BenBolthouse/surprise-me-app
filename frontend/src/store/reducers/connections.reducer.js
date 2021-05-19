/** @ignore */
const model = {
  requested: [],
  pending: [],
  approved: [],
};

const reducer = (state = model, { type, payload }) => {
  const stateCopy = { ...state };

  switch (type) {
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

    default:
      return state;
  }
};

export default reducer;
