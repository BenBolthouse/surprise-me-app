/**
 * Normalize an array to an object.
 * 
 * @param {*} array Input array; items must be objects and
 * contain an `id` integer property. Does not mutate the
 * input array.
 */
export const normalize = (array) => {
  const arrayCopy = [...array]
  const out = {}
  arrayCopy.forEach(item => out[item.id] = item)
  return out;
}

/**
 * Denormalize an object to an array.
 * 
 * @param {*} array Input array; items must be objects and
 * contain an `id` integer property. Does not mutate the
 * input object.
 */
export const denormalize = (obj) => {
  const objCopy = {...obj}
  const out = []
  objCopy.forEach(item => out.push(item))
  return out;
}
