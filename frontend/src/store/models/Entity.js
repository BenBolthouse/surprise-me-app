/**
 * Represents an abstract collection of entities.
 */
export class CollectionBase {
  /**
   * Represents an abstract collection of entities.
   *
   * @param {EntityBase} Entity Entity chosen for populating
   * @param {String} endpoint API endpoint to which requests are sent
   */
  constructor(Entity, endpoint) {
    this.Entity = Entity;
    this.endpoint = endpoint;
    this.collection = {};
  }

  /**
   * Initial collection population method creates entities in the
   * collection from a provided data array.
   *
   * Array should contain objects with keys and values that match entity
   * properties and property data types, as these will be overwritten on
   * the entity if present in the data array.
   *
   * Inheritors of `this.Entity` should implement a method `populate` that
   * maps key values to their entities, or otherwise an Error will be
   * thrown.
   *
   * Implicitly returns null.
   *
   * @param {Array<Object>} dataArray
   * @return {null} `null`
   */
  populateCollection(dataArray) {
    dataArray.forEach((item) => {
      const entity = new this.Entity(this.endpoint);

      entity.populateEntity(item);

      this.add(entity);
    });
  }

  /**
   * Returns collection filter results from predicates. Predicates are
   * lambda functions. All predicates provided must evaluate to true on a
   * single entity to survive the reckoning.
   *
   * If a single result is discovered then returns a single entity. If
   * multiple results are discovered then returns an object containing
   * entity results hashed with entity id's. If nothing is discovered then
   * returns null;
   *
   * @param {...Function} predicates
   * @return {Object | EntityBase | null} Collection of entities, single entity or null.
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
   * Adds the entity to the collection.
   *
   * Returns true.
   *
   * @param {EntityBase} entity
   * @return {true} `true`
   */
  add(entity) {
    this.collection[entity.id] = entity;
    return true;
  }

  /**
   * Deletes the entity from the collection.
   *
   * Implicitly returns null.
   *
   * @param {EntityBase} entity
   * @return {null} `null`
   */
  remove(entity) {
    delete this.collection[entity.id];
  }

  /**
   * Returns the stateful representation of the collection object.
   *
   * @return {Object} State object
   */
  state() {
    return Object.assign({}, this);
  }
}

/**
 * Extension of CollectionBase providing functionality for synchronizing
 * state with browser localStorage.
 */
export class LocalStorageBase extends CollectionBase {
  /**
   * Extension of CollectionBase providing functionality for synchronizing
   * state with browser localStorage.
   *
   * @param {EntityBase} Entity Entity chosen for populating
   * @param {String} endpoint API endpoint to which requests are sent
   * @param {String} localStorageKey Name of storage object to sync
   */
  constructor(Entity, endpoint, localStorageKey) {
    super(Entity, endpoint);

    // This checks if localstorage already has the storage object in
    // question. If it does then it'll attempt to sync with the object. If
    // not then it'll create it.
    const storageObj = window.localStorage.getItem(localStorageKey);

    this.localStorageKey = localStorageKey;

    if (storageObj) this.syncFromLocalStorage(JSON.parse(storageObj));
    else {
      const stringified = JSON.stringify(this.state());

      window.localStorage.setItem(localStorageKey, stringified);
    }
  }

  /**
   * Synchronize localStorage object from collection state.
   *
   * Returns true.
   *
   * @return {true} `true`
   */
  syncToLocalStorage() {
    const stringified = JSON.stringify(this.state());

    window.localStorage.setItem(this.localStorageKey, stringified);

    return true;
  }

  /**
   * Synchronize collection state from localStorage object.
   *
   * Returns true.
   *
   * @return {true} `true`
   */
  syncFromLocalStorage() {
    const stringified = window.localStorage.getItem(this.localStorageKey);

    const parsed = JSON.parse(stringified);

    this.populateCollection(Object.values(parsed.collection));

    return true;
  }
}

/**
 * Represents an abstract entity.
 *
 * @param {String} endpoint API endpoint to which requests are sent
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

  /**
   * Populates entity properties from data object's key values.
   *
   * Data object should contain keys and values that match entity
   * properties and property data types, as these will be overwritten on
   * the entity if present in the data array.
   *
   * Inheritors of `this.Entity` should implement a method `populate` that
   * maps key values to their entities, or otherwise an Error will be
   * thrown.
   *
   * Implicitly returns null.
   *
   * @param {Object} dataObject
   */
  populateEntity(dataObject) {
    const { id, type, created_at, updated_at, deleted_at } = dataObject;

    // prettier-ignore
    try {
      this.populate(dataObject);
    }
    catch (e) {
      throw Error("Children of EntityBase must implement a populate method.");
    }

    // If the child class extends dismissible base class then run that
    // populate method, as well.
    if (this.populateDismissible) this.populateDismissible(dataObject);

    this.id = id || this.id;
    this.type = type || this.type;
    this.createdAt = created_at || this.createdAt;
    this.updatedAt = updated_at || this.updatedAt;
    this.deletedAt = deleted_at || this.deletedAt;
  }

  /**
   * Returns the stateful representation of the entity object.
   *
   * @return {Object} State object
   */
  state() {
    return Object.assign({}, this);
  }
}

/**
 * Extension of base class EntityBase providing additional seen and
 * dismissed properties.
 */
export class DismissibleBase extends EntityBase {
  /**
   * Extension of base class EntityBase providing additional seen and
   * dismissed properties.
   */
  constructor() {
    super();
    this.seenAt = null;
    this.dismissedAt = null;
  }

  /**
   * Populates seen and dismissed properties automatically by inheritance
   * of EntityBase. You shouldn't need to have to use or invoke this
   * method.
   *
   * Implicitly returns null.
   *
   * @param {Object} config
   * @return {null} `null`
   */
  populateDismissible({ seen_at, dismissed_at }) {
    this.seenAt = seen_at || this.createdAt;
    this.dismissedAt = dismissed_at || this.dismissedAt;
  }
}
