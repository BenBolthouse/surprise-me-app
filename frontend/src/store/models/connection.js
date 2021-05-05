import { CollectionBase, EntityBase } from "./base";

/**
 * Represents a collection of connection entities.
 */
export class ConnectionsCollection extends CollectionBase {
  /**
   * Represents a collection of connection entities.
   */
  constructor() {
    super(Connection, "/api/v1/connections");
    this.userId = null;
    this.pending = {};
    this.requested = {};
    this.approved = {};
  }

  /**
   * Override to base class `populateCollection` that adds connections to
   * collections.
   *
   * @param {object} responseData
   */
  populateCollection(responseData) {
    responseData.forEach((item) => {
      const entity = new this.Entity(this.endpoint);
      entity.populateEntity(item);
      this.add(entity);
    });
    this.pending = this.filter(
      (x) => x.requestorId !== this.userId,
      (x) => x.approvedAt === null
    );
    this.requested = this.filter(
      (x) => x.requestorId === this.userId,
      (x) => x.approvedAt === null
    );
    this.approved = this.filter((x) => x.approvedAt !== null);
  }

  /**
   * Adds a connection to the requested collection.
   *
   * @param {Connection} connection
   */
  addRequested(connection) {
    this.add(connection);
    this.requested[connection.id] = connection;
  }

  /**
   * Adds a connection to the pending collection.
   *
   * @param {Connection} connection
   */
  addPending(connection) {
    this.add(connection);
    this.pending[connection.id] = connection;
  }

  /**
   * Searches the pending collection for the connection. If found then
   * removes the connection from pending and adds it to the approved
   * collection. If not found then adds the connection to the base class
   * collection and the approved collection.
   *
   * @param {Connection} connection
   */
  movePendingToApproved(connection) {
    // Method first searches the pending collection for the connection. If
    // not found then the method adds the connection argument to both the
    // base class collection and the approved collection.
    const pending = this.pending[connection.id];

    if (pending) {
      this.approved[connection.id] = pending;
      delete this.pending[connection.id];
      return;
    }

    this.add(connection);
    this.approved[connection.id] = connection;
  }

  /**
   * Removes a connection from the base class collection and all other
   * collections.
   *
   * @param {Connection} connection
   */
  removeFromAllCollections(connection) {
    const collection = this.collection[connection.id];
    const pending = this.pending[connection.id];
    const requested = this.requested[connection.id];
    const approved = this.approved[connection.id];

    if (collection) delete this.collection[connection.id];
    if (pending) delete this.pending[connection.id];
    if (requested) delete this.requested[connection.id];
    if (approved) delete this.approved[connection.id];
  }
}

/**
 * Represents a connection entity.
 */
export class Connection extends EntityBase {
  /**
   * Represents a connection entity.
   */
  constructor() {
    super();
    this.requestorId = null;
    this.otherUser = null;
    this.approvedAt = null;
  }

  /**
   * Method required by base class for populating data from api responses.
   *
   * @param {object} responseData
   */
  populate({ requestor_id, other_user, approved_at }) {
    this.requestorId = requestor_id;
    this.otherUser = other_user;
    this.approvedAt = approved_at;
  }
}
