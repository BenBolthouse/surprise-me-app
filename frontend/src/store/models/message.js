import { CollectionBase, DismissibleBase } from "./Entity";

/**
 * Extension of base collection class contains message collections hashed
 * by collection id.
 */
export class MessageManager extends CollectionBase {
  /**
   * Extension of base collection class contains message collections hashed
   * by collection id.
   */
  constructor() {
    super(MessagesCollection, "/api/v1/connections");
  }

  /**
   * Finds a message collection with a given ID and optionally updates the
   * collection's offset using the offset argument.
   *
   * @param {Number} connectionId
   * @param {Number} offset Offset of messages for response
   * @return {MessagesCollection | null} Message collection if found by ID or null if undefined.
   */
  getOrCreateMessageCollection(connectionId) {
    let collection = this.collection[connectionId];
    if (!collection) {
      collection = new MessagesCollection(connectionId);
      this.collection[connectionId] = collection;
    }
    return collection;
  }

  /**
   * Override to base class `populateCollection` to account for nested
   * collection.
   *
   * @param {object} responseData
   */
  populateCollection(responseData) {
    // Rather than running populate update on the message manager, the override
    // will search the collection for a message collection and run populate
    // on the message collection. If not found then will create a new
    // message collection and populate it.
    const { connection_id, messages } = responseData;
    let collection = this.collection[connection_id];
    if (!collection) {
      collection = new MessagesCollection(connection_id);
      this.collection[connection_id] = collection;
    }
    collection.populateCollection(messages);
  }
}

/**
 * Represents a collection of message entities.
 */
export class MessagesCollection extends CollectionBase {
  /**
   * Represents a collection of message entities.
   */
  constructor(connectionId) {
    super(Message, `/api/v1/connections/${connectionId}/messages`);
    this.connectionId = connectionId;
    this.offset = 0;
  }

  /**
   * Override to base class `add` the adds the connectionId to the message.
   *
   * @param {Message} message
   */
  add(message) {
    message.connectionId = this.connectionId;
    this.collection[message.id] = message;
  }
}

/**
 * Represents a message entity.
 */
export class Message extends DismissibleBase {
  /**
   * Represents a message entity.
   */
  constructor() {
    super();
    this.connectionId = null;
    this.sender = null;
    this.body = null;
    this.action = null;
    this.visibility = null;
    this.pending = false;
  }

  /**
   * Method required by base class for populating data from api responses.
   *
   * @param {object} responseData
   */
  populate({ sender, body, action, visibility, pending }) {
    this.sender = sender || this.sender;
    this.body = body || this.body;
    this.action = action || this.action;
    this.visibility = visibility || this.visibility;
    this.pending = pending || this.pending;
  }
}
