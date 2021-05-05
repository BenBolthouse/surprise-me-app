/**
 * Represents a collection of entities.
 */
export class CollectionBase {
  constructor(entity, endpoint) {
    this._entity = entity;
    this._endpoint = endpoint;
    this._collection = {};
  }

  get Entity() {
    return this._entity;
  }
  get endpoint() {
    return this._endpoint;
  }
  get collection() {
    return this._collection;
  }

  populateCollection(responseData) {
    responseData.forEach((item) => {
      const entity = new this.Entity(this._endpoint);
      entity.populateEntity(item);
      this.add(entity);
    });
  }

  filter(...predicates) {
    const out = {};
    for (const key in this._collection) {
      let prop = this._collection[key];
      let result = true;
      predicates.forEach((predicate) => {
        result = result ? predicate(prop) : false;
      });
      if (result) out[key] = prop;
    }
    return out;
  }

  add(entity) {
    this._collection[entity.id] = entity;
  }

  state() {
    return Object.assign({}, this);
  }
}

/**
 * Represents a single entity.
 */
export class EntityBase {
  constructor(endpoint) {
    this._endpoint = endpoint;
    this._id = null;
    this._type = null;
    this._createdAt = null;
    this._updatedAt = null;
    this._deletedAt = null;
  }

  get endpoint() {
    return this._endpoint;
  }
  get id() {
    return this._id;
  }
  get type() {
    return this._type;
  }
  get createdAt() {
    return new Date(this._createdAt);
  }
  get updatedAt() {
    return new Date(this._updatedAt);
  }
  get deletedAt() {
    return new Date(this._deletedAt);
  }
  get isDeleted() {
    return this._deletedAt !== null;
  }

  populateEntity(responsePayload) {
    const { id, type, created_at, updated_at, deleted_at } = responsePayload;

    // Try a population on child class populate method. It's up to the dev
    // to write these populate methods on the child classes. Without it
    // this method will throw an error.
    try {
      this.populate(responsePayload);
    } catch (e) {
      throw Error("Children of EntityBase must implement a populate method.");
    }

    // If the child class extends dismissible base class then run that
    // populate method, as well.
    if (this.populateDismissible) {
      this.populateDismissible(responsePayload);
    }

    this._id = id || this._id;
    this._type = type || this._type;
    this._createdAt = created_at || this._createdAt;
    this._updatedAt = updated_at || this._updatedAt;
    this._deletedAt = deleted_at || this._deletedAt;
  }

  state() {
    return Object.assign({}, this);
  }
}

/**
 * Represents an entity which can be seen and/or dismissed by a user.
 */
export class DismissibleBase extends EntityBase {
  constructor() {
    super();
    this._seenAt = null;
    this._dismissedAt = null;
  }

  get seenAt() {
    return new Date(this._seenAt);
  }
  get isSeen() {
    return this._seenAt !== null;
  }
  get dismissedAt() {
    return new Date(this._dismissedAt);
  }
  get isDismissed() {
    return this._dismissedAt !== null;
  }

  populateDismissible({ seen_at, dismissed_at }) {
    this._seenAt = seen_at || this._createdAt;
    this._dismissedAt = dismissed_at || this._dismissedAt;
  }
}
