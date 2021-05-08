/** @module store/models/ui-notification */

import { EntityBase, EntityLocalStorageBase } from "./Entity";

// for applying iterative z-index to notifications as they are created
const Z_INDEX_LOWER_BOUND = 300;
const Z_INDEX_UPPER_BOUND = 400;
let _zIndexCounter = 300;

/**
 * @class
 * @abstract
 * @classdesc Represents a collection of UI notifications.
 */
export class UINotificationCollection extends EntityLocalStorageBase {
  /** @returns {this} */
  constructor() {
    super(UINotification, null, "notifications_ui");

    return this;
  }

  /**
   * Adds a UI notification to the collection.
   * @param {Notification} notification
   * @return {true}
   */
  add(notification) {
    if (_zIndexCounter > Z_INDEX_UPPER_BOUND) _zIndexCounter = Z_INDEX_LOWER_BOUND;

    notification.id = _createHashId();
    
    notification.zIndex = _zIndexCounter;

    _zIndexCounter ++;
    
    this.collection[notification.id] = notification;
    
    return true;
  }
}

/**
 * @class
 * @classdesc Represents a UI notification.
 */
export class UINotification extends EntityBase {
  /** @returns {this} */
  constructor() {
    super();
    this.body = null;
    this.zIndex = null;

    return this;
  }

  /**
   * Updates the UI notification from a data object with mappable key value pairs.
   * @param {object} data
   * @return {this}
   */
  update({ body, zIndex }) {
    this.body = body || this.body;
    this.zIndex = zIndex || this.zIndex;

    return this;
  }
}

/** @ignore */
function _createHashId() {
  const LENGTH = 8;
  const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let out = "";

  for (let i = 0; i < LENGTH; i++) {
    let idx = Math.floor(Math.random() * CHARS.length)
    out += CHARS[idx]
  }

  return out;
}
