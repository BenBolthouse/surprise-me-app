/** @module store/models/product */

import { EntityBase, EntityCollectionBase } from "./Entity";

/**
 * @class
 * @classdesc Represents a collection of products.
 */
export class ProductCollection extends EntityCollectionBase {
  constructor() {
    super(Product, "/api/v1/products")
  }
}

/**
 * @class
 * @classdesc Represents a product.
 */
export class Product extends EntityBase {
  constructor() {
    super();
    this.name = null;
    this.description = null;
    this.price = null;
    this.latitude = null;
    this.longitude = null;
  }

  /**
   * Updates the product from a data object with mappable key value pairs.
   * @param {object} data
   * @return {this}
   */
  update({name,description,price,latitude,longitude}) {
    this.name = name ? name : this.name;
    this.description = description ? description : this.description;
    this.price = price ? price : this.price;
    this.latitude = latitude ? latitude : this.latitude;
    this.longitude = longitude ? longitude : this.longitude;

    return this;
  }
}
