import { EntityBase, LocalStorageBase } from "./Entity";

// for applying iterative z-index to notifications as they are created
const Z_INDEX_LOWER_BOUND = 300;
const Z_INDEX_UPPER_BOUND = 400;
let _zIndexCounter = 300;

/**
 * Represents a collection UI notifications.
 */
export class UINotificationCollection extends LocalStorageBase {
  /**
   * Represents a collection UI notifications.
   */
  constructor() {
    // Endpoint is null because UI notifications don't sync state with the
    // database. UI notifications are generated from response results and
    // RESTless internal events and are then persisted to localstorage.
    super(UINotification, null, "notifications_ui");
  }

  /**
   * Override to base class `add()` which handles incrementing a z-index
   * counter for UI purposes.
   *
   * Returns true.
   *
   * @param {EntityBase} entity
   * @return {true} `true`
   */
  add(entity) {
    if (_zIndexCounter > Z_INDEX_UPPER_BOUND) _zIndexCounter = Z_INDEX_LOWER_BOUND;

    entity.id = _createHashId();
    
    entity.zIndex = _zIndexCounter;

    _zIndexCounter ++;
    
    this.collection[entity.id] = entity;
    
    return true;
  }
}

/**
 * Represents a UI notification.
 */
export class UINotification extends EntityBase {
  /**
   * Represents a UI notification.
   */
  constructor() {
    super();
    this.body = null;
    this.zIndex = null;
  }

  /**
   * Method required by base class.
   * 
   * Implicitly returns null.
   *
   * @param {object} dataObject
   * @return {null} `null`
   */
  populate({ body, zIndex }) {
    this.body = body || this.body;
    this.zIndex = zIndex || this.zIndex;
  }
}

/**
 * Private function generates random hash for notification keys.
 */
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
