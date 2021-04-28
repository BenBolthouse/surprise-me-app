/**
 * Normalize an array to an object.
 * 
 * @param {*} array Input array; items must be objects and
 * contain an `id` integer property. Does not mutate the
 * input array.
 */
export const normalize = (array, prop) => {
  const arrayCopy = [...array]
  const out = {}
  if (prop) {
    arrayCopy.forEach(item => out[item[prop]] = item)
  }
  else {
    arrayCopy.forEach(item => out[item.id] = item)
  }
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
  const out = []
  for (const v of Object.values(obj)) out.push(v);
  return out;
}
