import validate from "validate.js";

class EntityBase {
  constructor(schema, options) {
    // prettier-ignore
    if (options.randomHashId === true) {
      this.id = _randomHashId(options.randomHashLength);
    }
    else this.id = null;

    this.collection = null;

    Object.keys(schema).forEach((prop) => {
      this[prop] = null;
    });

    this.createdAt = null;
    this.updatedAt = null;
    this.deletedAt = null;
    this.validation = {
      _init: null,
      _schema: null,
    };

    if (options.validation === true) {
      this.validation = {
        passed: false,
        show: false,
        results: {},
        _init: {},
        _schema: options.validationSchema,
      };
      options.validationProps.forEach((prop) => {
        this.validation.results[prop] = [];
        this.validation._init[prop] = [];
      });
    }

    this._options = options;
    this._schema = {
      id: "Number | String",
      createdAt: "Date",
      updatedAt: "Date",
      deletedAt: "Date",
      ...schema,
    };
    this._validationProps;
  }

  setCreatedAt() {
    this.createdAt = new Date();

    return this;
  }

  setUpdatedAt() {
    this.updatedAt = new Date();

    return this;
  }

  setDeletedAt() {
    this.deletedAt = new Date();

    return this;
  }

  update(props) {
    if (!this.id && this._options.randomHashId === true) {
      this.id = _randomHashId(this._options.randomHashLength);
    }

    Object.entries(props).forEach(([key, val]) => {
      if (this[key] === null || this[key]) this[key] = val;
    });

    return this;
  }

  return() {
    let output = { ...this };

    delete output._options;

    return output;
  }

  returnNonCircular() {
    let output = { ...this };

    delete output.validation;
    delete output.collection;
    delete output._options;

    return output;
  }

  returnProps() {
    const output = {};

    Object.keys(this._schema).forEach(prop => {
      output[prop] = this[prop];
    });

    return output;
  }

  validate(props) {
    let attrs = {};
    let schema = {};

    // prettier-ignore
    if (Array.isArray(props)) {
      props.forEach((prop) => {
        attrs[prop] = this[prop];

        schema[prop] = this.validation._schema[prop];
      });
    }
    else {
      Object.keys(this.validation.results).forEach((prop) => {
        attrs[prop] = this[prop];
      });

      schema = this.validation._schema;
    }


    const result = validate(attrs, schema);

    this.validation.passed = result ? false : true;

    this.validation.results = result
      ? { ...this.validation.results, ...result }
      : this.validation._init;

    return this;
  }

  showValidation(show) {
    this.validation.show = show;

    return this;
  }

  resetValidation() {
    this.validation.passed = false;

    this.validation.results = this.validation._init;

    return this;
  }
}

const _randomHashId = (length) => {
  let output = "";

  const chars =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

  for (let i = 0; i < length; i++) {
    const idx = Math.floor(Math.random() * chars.length);

    output += chars[idx];
  }

  return output;
};

export default EntityBase;
