class Manager {
  constructor(collections) {
    this.collections = {};

    Object.keys(collections).forEach((key) => {
      collections[key].manager = this;

      this.collections[collections[key].name] = collections[key];
    });
  }

  collection(name) {
    return Object.values(this.collections).find((x) => x.name === name);
  }

  moveToCollection(entity, source, destination) {
    const src = this.collection(source);

    let ent = src.entity((x) => x.id === entity.id);

    ent = this.collection(destination).createEntity(ent);

    delete src.entities[entity.id];

    return ent;
  }

  copyToCollection(entity, source, destination) {
    const src = this.collection(source);

    let ent = src.entity((x) => x.id === entity.id);

    ent = this.collection(destination).createEntity(ent);

    return ent;
  }

  removeFromCollections(entity) {
    Object.keys(this.collections).forEach((key) => {
      delete this.collections[key].entities[entity.id];
    });
  }

  return() {
    return { ...this };
  }
}

export default Manager;
