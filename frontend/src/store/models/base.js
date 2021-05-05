/**
 * Represents a collection of entities.
 */
export class CollectionBase {
  constructor(Entity, endpoint) {
    this.Entity = Entity;
    this.endpoint = endpoint;
    this.collection = {};
  }

  populateCollection(responseData) {
    responseData.forEach((item) => {
      const entity = new this.Entity(this.endpoint);
      entity.populateEntity(item);
      this.add(entity);
    });
  }

  filter(...predicates) {
    const out = {};
    for (const key in this.collection) {
      let prop = this.collection[key];
      let result = true;
      predicates.forEach((predicate) => {
        result = result ? predicate(prop) : false;
      });
      if (result) out[key] = prop;
    }
    return out;
  }

  add(entity) {
    this.collection[entity.id] = entity;
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
    this.endpoint = endpoint;
    this.id = null;
    this.type = null;
    this.createdAt = null;
    this.updatedAt = null;
    this.deletedAt = null;
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

    this.id = id || this.id;
    this.type = type || this.type;
    this.createdAt = created_at || this.createdAt;
    this.updatedAt = updated_at || this.updatedAt;
    this.deletedAt = deleted_at || this.deletedAt;
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
    this.seenAt = null;
    this.dismissedAt = null;
  }

  populateDismissible({ seen_at, dismissed_at }) {
    this.seenAt = seen_at || this.createdAt;
    this.dismissedAt = dismissed_at || this.dismissedAt;
  }
}
