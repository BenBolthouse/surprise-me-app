/** @module store/models/entity */

/**
 * @class
 * @abstract
 * @classdesc Abstract class representing a collection of entities.
 */
export class EntityCollectionBase {
  /**
   * @param {EntityBase} Entity Entity managed by this collection
   * @param {String} endpoint API endpoint to which requests are sent
   * @returns {this}
   */
  constructor(Entity, endpoint) {
    this.Entity = Entity;
    this.endpoint = endpoint;
    this.collection = {};

    return this;
  }

  /**
   * Creates the initial collection of entities from an array of mappable
   * data objects.
   * @param {Array<Object>} data
   * @returns {this}
   */
  produceFrom(data) {
    data.forEach((item) => {
      this.add(new this.Entity(this.endpoint).produceEntityFrom(item));
    });

    return this;
  }

  /**
   * Returns entities filtered by predicates.
   * @param {...Function} predicates
   * @returns {object | EntityBase | null} If a single entity is filtered
   * from the collection then that entity will be returned. If multiple
   * entities are filtered then those entities will be returned in an
   * object with each entity's id attribute being the key and the entity
   * being the value. If no entities are filtered then null will be
   * returned.
   */
  filter(...predicates) {
    const out = {};
    let counter = 0;
    let last;

    for (const key in this.collection) {
      let prop = this.collection[key];
      let result = true;

      predicates.forEach((predicate) => {
        result = result ? predicate(prop) : false;
      });

      if (result) {
        out[key] = prop;

        counter++;

        last = prop;
      }
    }

    if (counter > 1) return out;
    else if (counter == 1) return last;

    return null;
  }

  /**
   * Adds an entity to the collection.
   * @param {EntityBase} entity
   * @returns {true}
   */
  add(entity) {
    this.collection[entity.id] = entity;

    return true;
  }

  /**
   * Removes an entity from the collection.
   * @param {EntityBase} entity
   * @returns {true}
   */
  remove(entity) {
    delete this.collection[entity.id];

    return true;
  }

  /**
   * Returns a Redux state copy.
   * @returns {object} Copy of the collection.
   */
  copy() {
    return Object.assign({}, this);
  }
}

/**
 * @class
 * @abstract
 * @classdesc Abstract class extends CollectionBase to provide additional
 * support for browser local storage state persistence.
 */
export class EntityLocalStorageBase extends EntityCollectionBase {
  /**
   * @param {EntityBase} Entity Entity managed by this collection
   * @param {String} endpoint API endpoint to which requests are sent
   * @param {String} localStorageKey Name of local storage object
   * @returns {this}
   */
  constructor(Entity, endpoint, localStorageKey) {
    super(Entity, endpoint);

    this.localStorageKey = localStorageKey;

    // This checks if localstorage already has the storage object in
    // question. If it does then it'll attempt to sync with the object. If
    // not then it'll create it.
    const storageObj = window.localStorage.getItem(localStorageKey);

    if (storageObj) this.syncFromLocalStorage(JSON.parse(storageObj));
    else {
      const stringified = JSON.stringify(this.copy());

      window.localStorage.setItem(localStorageKey, stringified);
    }

    return this;
  }

  /**
   * Synchronizes localStorage object from collection state.
   * @returns {true}
   */
  syncToLocalStorage() {
    const stringified = JSON.stringify(this.copy());

    window.localStorage.setItem(this.localStorageKey, stringified);

    return true;
  }

  /**
   * Synchronizes collection state from localStorage object, selecting only
   * notifications that have not yet been dismissed.
   * @returns {true}
   */
  syncFromLocalStorage() {
    const stringified = window.localStorage.getItem(this.localStorageKey);

    const parsed = JSON.parse(stringified);

    let notifications = Object.values(parsed.collection);

    notifications = notifications.filter(x => x.dismissedAt === null)

    this.produceFrom(notifications);

    return true;
  }
}

/**
 * @class
 * @abstract
 * @classdesc Abstract class representing an entity.
 */
export class EntityBase {
  /**
   * @param {String} endpoint API endpoint to which requests are sent
   * @returns {this}
   */
  constructor(endpoint) {
    this.endpoint = endpoint;
    this.id = null;
    this.type = null;
    this.createdAt = null;
    this.updatedAt = null;
    this.deletedAt = null;

    return this;
  }

  /**
   * Updates an entity from a data object with mappable key value pairs.
   * @param {object} data
   * @returns {this}
   */
  produceEntityFrom(data) {
    const { id, type, createdAt, updatedAt, deletedAt } = data;

    // prettier-ignore
    try {
      this.update(data);
    }
    catch (e) {
      throw Error("Children of EntityBase must implement an update method.");
    }

    if (this.produceDismissibleFrom) this.produceDismissibleFrom(data);

    this.id = id || this.id;
    this.type = type || this.type;
    this.createdAt = createdAt || this.createdAt;
    this.updatedAt = updatedAt || this.updatedAt;
    this.deletedAt = deletedAt || this.deletedAt;

    return this;
  }

  /**
   * Returns a Redux state copy.
   * @returns {object} Copy of the entity.
   */
  copy() {
    return Object.assign({}, this);
  }
}

/**
 * @class
 * @abstract
 * @classdesc Abstract class extends EntityBase to provide additional
 * functionality for marking entities as seen and/or dismissed by a user.
 */
export class EntityDismissibleBase extends EntityBase {
  constructor() {
    super();
    this.seenAt = null;
    this.dismissedAt = null;
  }

  /**
   * Marks an entity as dismissed by the user.
   * @returns {this}
   */
  dismiss() {
    const date = new Date().toISOString();

    if (!this.seenAt) this.seenAt = date;

    this.dismissedAt = date;

    return this;
  }

  /**
   * Marks an entity as seen by the user.
   * @returns {this}
   */
  see() {
    this.seenAt = new Date().toISOString();

    return this;
  }

  /**
   * Updates a dismissible entity from a data object with mappable key value pairs.
   * @param {Object} config
   * @return {null} `null`
   */
  produceDismissibleFrom({ seenAt, dismissedAt }) {
    this.seenAt = seenAt || this.createdAt;
    this.dismissedAt = dismissedAt || this.dismissedAt;
  }
}
