/** @module store/models/message */

import { EntityCollectionBase, EntityDismissibleBase } from "./Entity";

/**
 * @class
 * @abstract
 * @classdesc Represents a managed collection of message collections.
 */
export class MessageManager extends EntityCollectionBase {
  /** @returns {this} */
  constructor() {
    super(MessagesCollection, "/api/v1/connections");

    return this;
  }

  /**
   * Returns a message collection or creates one by default.
   * @param {Number} connectionId
   * @return {MessagesCollection | true}
   */
  getOrCreateMessagesCollection(connectionId) {
    let collection = this.collection[connectionId];

    if (!collection) {
      collection = new MessagesCollection(connectionId);

      this.collection[connectionId] = collection;
    }

    return collection || true;
  }

  /**
   * Returns a message collection or false if not found.
   * @param {Number} connectionId
   * @return {MessagesCollection | false}
   */
  getMessagesCollection(connectionId) {
    return this.collection[connectionId] || false;
  }

  /**
   * Override to base class method produceFrom searches collection for a message
   * collection and then runs the collection's init method using the data
   * argument. If the message collection is not found then the collection
   * will be created first before running the init method.
   * @param {object} data
   * @returns {MessagesCollection} The found or created collection
   */
  produceFrom(data) {
    const { connectionId, messages } = data;

    let collection = this.collection[connectionId];

    if (!collection) {
      collection = new MessagesCollection(connectionId);

      this.collection[connectionId] = collection;
    }

    collection.produceFrom(messages);

    return collection;
  }
}

/**
 * @class
 * @classdesc Represents a collection of message entities.
 */
export class MessagesCollection extends EntityCollectionBase {
  /**
   * @param {Number} connectionId
   * @returns {this}
   */
  constructor(connectionId) {
    super(Message, `/api/v1/connections/${connectionId}/messages`);
    this.connectionId = connectionId;
    this.offset = 0;

    return this;
  }

  /**
   * Adds a message to the collection.
   * @param {Message} message
   * @returns {true}
   */
  add(message) {
    message.connectionId = this.connectionId;

    this.collection[message.id] = message;

    return true;
  }

  /**
   * Gets a message by ID or returns false.
   * @param {Number} messageId
   * @returns {Message | false}
   */
  getMessage(messageId) {
    const message = this.collection[messageId];

    return message || false;
  }
}

/**
 * @class
 * @classdesc Represents a message entity.
 */
export class Message extends EntityDismissibleBase {
  /** @returns {this} */
  constructor() {
    super();
    this.connectionId = null;
    this.sender = null;
    this.body = null;
    this.action = null;
    this.visibility = null;
    this.pending = false;

    return this;
  }

  /**
   * Updates a message from a data object with mappable key value pairs.
   * @param {object} data
   * @returns {this}
   */
  update({ sender, body, action, visibility, pending }) {
    this.sender = sender || this.sender;
    this.body = body || this.body;
    this.action = action || this.action;
    this.visibility = visibility || this.visibility;
    this.pending = pending || this.pending;

    return this
  }
}
