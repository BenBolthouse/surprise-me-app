/** @module store/models/connection */

import { EntityCollectionBase, EntityBase } from "./Entity";

/**
 * @class
 * @classdesc Represents a collection of connections.
 */
export class ConnectionsCollection extends EntityCollectionBase {
  constructor() {
    super(Connection, "/api/v1/connections");
    this.userId = null;
    this.pending = {};
    this.requested = {};
    this.approved = {};
  }

  /**
   * Override to base class method produceFrom that adds connections to
   * collections.
   * @param {object} data
   * @returns {this}
   */
  produceFrom(data) {
    data.forEach((item) => {
      this.add(new this.Entity(this.endpoint).produceEntityFrom(item));
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

    return this;
  }

  /**
   * Adds a connection to the requested collection.
   * @param {Connection} connection
   * @returns {true}
   */
  addRequested(connection) {
    this.add(connection);
    this.requested[connection.id] = connection;

    return true;
  }

  /**
   * Adds a connection to the pending collection.
   * @param {Connection} connection
   * @returns {true}
   */
  addPending(connection) {
    this.add(connection);
    this.pending[connection.id] = connection;

    return true;
  }

  /**
   * Moves a pending connection to approved. If the connection is not found
   * in pending then the connection will automatically be created in both
   * the default and approved collections.
   * @param {Connection} connection
   * @returns {true | false} Returns true if the connection was found and
   * moved from pending to approved and returns false if the connection was
   * not found and was instead created in the default and approved
   * collections.
   */
  movePendingToApproved(connection) {
    const pending = this.pending[connection.id];

    if (pending) {
      this.approved[connection.id] = pending;
      delete this.pending[connection.id];
      return;
    }

    this.add(connection);
    this.approved[connection.id] = connection;

    return pending ? true : false;
  }

  /**
   * Removes a connection from all collections.
   * @param {Connection} connection
   * @returns {true}
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

    return true;
  }
}

/**
 * @class
 * @classdesc Represents a connection entity.
 */
export class Connection extends EntityBase {
  constructor() {
    super();
    this.requestorId = null;
    this.otherUser = null;
    this.approvedAt = null;
    this.otherUserComposing = false;
  }

  /**
   * Updates the connection from a data object with mappable key value pairs.
   * @param {object} data
   * @returns {this}
   */

  // prettier-ignore
  update({ requestorId, otherUser, approvedAt, userComposing }) {
    this.requestorId = requestorId || this.requestorId;
    this.otherUser = otherUser || this.otherUser;
    this.approvedAt = approvedAt || this.approvedAt;
    this.otherUserComposing = userComposing !== undefined ? userComposing : this.otherUserComposing;

    return this;
  }
}
