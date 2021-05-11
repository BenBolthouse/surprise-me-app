/** @module store/models/notification */

import { EntityDismissibleBase, EntityLocalStorageBase } from "./Entity";

// for applying iterative z-index to notifications as they are created
const Z_INDEX_LOWER_BOUND = 300;
const Z_INDEX_UPPER_BOUND = 400;
let _zIndexCounter = 300;

/**
 * @class
 * @classdesc Represents a collection of UI notifications.
 */
export class UINotificationCollection extends EntityLocalStorageBase {
  constructor() {
    super(UINotification, null)
  }
}

/**
 * @class
 * @classdesc Represents a collection of session notifications.
 */
export class SessionNotificationCollection extends EntityLocalStorageBase {
  constructor() {
    super(SessionNotification, "/api/v1/notifications")
  }
}

/**
 * @class
 * @classdesc Represents a notification.
 */
export class Notification extends EntityDismissibleBase {
  /** @returns {this} */
  constructor() {
    super();
    this.id = this._createHashId();
    this.body = null;

    return this;
  }

  /**
   * Updates the UI notification from a data object with mappable key value pairs.
   * @param {object} data
   * @return {this}
   */
  update({ body, action }) {
    this.body = body || this.body;
    this.action = action || this.action;

    return this;
  }

  /** @ignore */
  _createHashId() {
    const LENGTH = 8;

    const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    let out = "";

    for (let i = 0; i < LENGTH; i++) {
      let idx = Math.floor(Math.random() * CHARS.length);

      out += CHARS[idx];
    }

    return out;
  }
}

/**
 * @class
 * @classdesc Represents a UI notification.
 */
export class UINotification extends Notification {
  /** @returns {this} */
  constructor() {
    super();

    // prettier-ignore
    if (_zIndexCounter !== Z_INDEX_UPPER_BOUND) {
      this.zIndex = _zIndexCounter;

      _zIndexCounter ++;
    }
    else {
      this.zIndex = Z_INDEX_LOWER_BOUND;

      _zIndexCounter = Z_INDEX_LOWER_BOUND;
    }

    return this;
  }

  /**
   * Updates the UI notification from a data object with mappable key value
   * pairs.
   * @param {object} data
   * @return {this}
   */
  update({ body, zIndex }) {
    this.body = body || this.body;
    this.zIndex = zIndex || this.zIndex;

    return this;
  }
}

/**
 * @class
 * @classdesc Represents a session notification.
 */
export class SessionNotification extends Notification {
  /** @returns {this} */
  constructor() {
    super();

    return this;
  }

  /**
   * Updates the session notification from a data object with mappable key
   * value pairs.
   * @param {object} data
   * @return {this}
   */
  update({ body }) {
    this.body = body || this.body;

    return this;
  }
}
