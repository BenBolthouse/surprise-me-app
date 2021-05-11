/** @module store/reducers/products */

import { api, handler } from "../..";
import { ProductCollection } from "../models/Product";
import { sessionManager } from "./session";

const productsManager = new ProductCollection();

const GET_PRODUCTS = "products ——————————> GET_PRODUCTS";

/**
 * Gets products for specified geocoordinates and radius.<br>
 *
 * coordinates:<br>
 *
 * `{ latitude, longitude, radius }`
 */
export const getProducts = (coordinates) => (dispatch) => handler(async () => {
  sessionManager.requireGeolocation();

  const action = (payload) => ({ type: GET_PRODUCTS, payload });

  const { latitude, longitude, radius } = coordinates;

  const endpoint = `${productsManager.endpoint}?lat=${latitude}&lon=${longitude}&rad=${radius}`;

  const { data } = await api.get(endpoint);

  dispatch(action(data));

  return true;
});

const reducer = (state = productsManager.copy(), { type, payload }) => {

  switch (type) {
    case GET_PRODUCTS:
      productsManager.produceFrom(payload);
      return productsManager.copy();

    default:
      return state;
  }
};

export default reducer;
