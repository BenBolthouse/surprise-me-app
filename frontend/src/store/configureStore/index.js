import { createStore, combineReducers } from "redux";

import enhancer from "../enhancer";

import reducers from "../reducers";

const rootReducer = combineReducers(reducers);

export function configureStore(preloadedState) {
  return createStore(rootReducer, preloadedState, enhancer);
}
