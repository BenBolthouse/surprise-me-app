class Collection {
  constructor({ name, model, syncToLocalStorage }) {
    this.name = name;
    this.model = model;
    this.entities = {};
    this.manager = null;

    if (syncToLocalStorage === true) {
      const exists = window.localStorage.getItem(this.name);

      if (exists) this.syncFromLocalStorage();
      else this.syncToLocalStorage();
    }
  }

  entity(predicate) {
    return Object.values(this.entities).find(predicate);
  }

  createEntity(props) {
    const entity = new this.model();

    entity.collection = this;

    entity.update(props);

    this.entities[entity.id] = entity;

    return entity;
  }

  createEntities(propsArray) {
    propsArray.forEach((props) => {
      const entity = new this.model();

      entity.collection = this;

      entity.update(props);

      this.entities[entity.id] = entity;
    });

    return this.entities;
  }

  syncToLocalStorage() {
    const stringified = JSON.stringify(this.returnNonCircular());

    window.localStorage.setItem(this.name, stringified);

    return this;
  }

  syncFromLocalStorage() {
    let storage = window.localStorage.getItem(this.name);

    storage = JSON.parse(storage);

    storage = Object.values(storage.entities);

    const entities = this.createEntities(storage);

    this.entities = { ...this.entities, ...entities };

    return this;
  }

  return() {
    let collection = { ...this };

    for (let key in collection.entities) {
      collection.entities[key] = collection.entities[key].return();
    }

    return collection;
  }

  returnNonCircular() {
    let collection = { ...this };

    delete collection.manager;

    for (let key in collection.entities) {
      collection.entities[key] = this.entities[key].returnNonCircular();
    }

    return collection;
  }
}

export default Collection;
