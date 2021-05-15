import { Collection, EntityBase, Manager } from "../entity";
import userManager from "./user.model";

class Connection extends EntityBase {
  constructor() {
    super(
      {
        requestorId: "Number",
        otherUser: "Object",
        otherUserComposing: "Boolean",
        approvedAt: "Date",
      },
      {}
    );
  }
}

const requestedConnectionsCollection = new Collection({
  name: "requested_connections",
  model: Connection,
});

const pendingConnectionsCollection = new Collection({
  name: "pending_connections",
  model: Connection,
});

const approvedConnectionsCollection = new Collection({
  name: "approved_connections",
  model: Connection,
});

const connectionsManager = new Manager({
  requestedConnectionsCollection,
  pendingConnectionsCollection,
  approvedConnectionsCollection,
});

connectionsManager.divvy = (connections) => {
  connectionsManager
    .collection("requested_connections")
    .createEntities(
      connections
        .filter((x) => x.requestorId === userManager.id)
        .filter((x) => x.approvedAt === null)
    );
  connectionsManager
    .collection("pending_connections")
    .createEntities(
      connections
        .filter((x) => x.requestorId !== userManager.id)
        .filter((x) => x.approvedAt === null)
    );
  connectionsManager
    .collection("approved_connections")
    .createEntities(connections.filter((x) => x.approvedAt !== null));
};

export default connectionsManager;
