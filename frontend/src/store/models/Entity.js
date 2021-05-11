/**
 * @module store/models/entity
 * @author Ben Bolthouse
 * @description Entity is a solution for writing too much boilerplate Redux
 * code.<br>
 *
 * I identified a trend in state management while I was writing the
 * components for the Surprise Me app: Redux thunk follows the same old
 * tried-and-true REST conventions. That is, Redux and Thunk manage
 * collections and entities using standard CRUD operations found in
 * REST.<br>
 *
 * There are big aspirations for this project, and big time-savings
 * implications with the new workflow that this library introduces. For
 * instance, let's analyze a typical, non-Entity Redux workflow:<br>
 *
 * 1. Create the reducer and add the reducer to the root reducer,
 * 1. Write an action and a thunk to transact with an API endpoint,
 * 1. Write a request body from thunk arguments to send to the API as an
 *    async fetch request,
 * 1. Retrieve and parse the data,
 * 1. Dispatch the data to the reducer as a payload,
 * 1. Reducer handles all state changes, potentially several more lines of
 *    code,
 * 1. Finally...the reducer returns the new copy of state.<br>
 *
 * While Redux gives the developer the flexibility for configuration, this
 * (in my mind) is far too much configuration for state changes that
 * predictably follow patterns.<br>
 *
 * Consider the new workflow introduced with Entity:<br>
 *
 * 1. Write a model that extends EntityCollectionBase (or variant of),
 * 1. Write a model that extends EntityBase (or variant of),
 * 1. Create the reducer and add the reducer to the root reducer,
 * 1. Write an action and a thunk to transact with an API endpoint,
 * 1. Use one of post, put, patch, get or delete instance methods from the
 *    collection to transfer state to the API,
 * 1. Dispatch the data to reducer as a payload,
 * 1. Reducer simply returns a copy of the collection (no state management
 *    is needed in the reducer, it has already been handled in the
 *    thunk).<br>
 *
 * You may notice that there isn't even a need for a reducer in this
 * workflow. Precisely! Future developments of Entity will do away with the
 * need to write the reducers *and* the actions *and* the thunks. At its
 * core, Entity will use Redux and Redux Thunk for powerful state
 * management tools. Entity will do away with the need to configure the
 * parts of Redux and Redux Thunk that ultimately follow patterns, so the
 * developer can focus their attention on the interface.
 *
 * Now finally, let's analyze what this will look like in a future version
 * of Entity:
 *
 * 1. Define your manager, collection and entity models in the
 *    entity.config.js file,
 * 1. Dispatch changes from frontend code using REST standards of post,
 *    put, patch, get and delete,
 * 1. Either receive a modified state object or a cached error message as a
 *    result.<br>
 *
 * So much simpler, eh? I'm excited to continue to develop this library so
 * I (and hopefully even you!) can stop writing excessive code. Until
 * then...cheers!
 */

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
