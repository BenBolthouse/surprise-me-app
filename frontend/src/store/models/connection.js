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
    this._userId = null;
    this._pending = {};
    this._requested = {};
    this._approved = {};
  }

  set userId(id) {
    this._userId = id;
  }

  /**
   * Override to base class `populateCollection` that adds connections to
   * collections.
   *
   * @param {object} responseData 
   */
  populateCollection(responseData) {
    responseData.forEach((item) => {
      const entity = new this.Entity(this._endpoint);
      entity.populateEntity(item);
      this.add(entity);
    });
    this._pending = this.filter(
      (x) => x._requestorId !== this._userId,
      (x) => x._approvedAt === null
    );
    this._requested = this.filter(
      (x) => x._requestorId === this._userId,
      (x) => x._approvedAt === null
    );
    this._approved = this.filter((x) => x._approvedAt !== null);
  }

  /**
   * Adds a connection to the requested collection.
   *
   * @param {Connection} connection
   */
  addRequested(connection) {
    this.add(connection);
    this._requested[connection.id] = connection;
  }

  /**
   * Adds a connection to the pending collection.
   *
   * @param {Connection} connection
   */
  addPending(connection) {
    this.add(connection);
    this._pending[connection.id] = connection;
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
    const pending = this._pending[connection.id];

    if (pending) {
      this._approved[connection.id] = pending;
      delete this._pending[connection.id];
      return;
    }

    this.add(connection);
    this._approved[connection.id] = connection;
  }

  /**
   * Removes a connection from the base class collection and all other
   * collections.
   *
   * @param {Connection} connection
   */
  removeFromAllCollections(connection) {
    const collection = this._collection[connection.id];
    const pending = this._pending[connection.id];
    const requested = this._requested[connection.id];
    const approved = this._approved[connection.id];

    if (collection) delete this._collection[connection.id];
    if (pending) delete this._pending[connection.id];
    if (requested) delete this._requested[connection.id];
    if (approved) delete this._approved[connection.id];
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
    this._requestorId = null;
    this._otherUser = null;
    this._approvedAt = null;
  }

  get requestorId() {
    return this._requestorId;
  }
  get otherUser() {
    return this._otherUser;
  }
  get approvedAt() {
    return this._approvedAt;
  }

  /**
   * Method required by base class for populating data from api responses.
   *
   * @param {object} responseData 
   */
  populate({ requestor_id, other_user, approved_at }) {
    this._requestorId = requestor_id;
    this._otherUser = other_user;
    this._approvedAt = approved_at;
  }
}
