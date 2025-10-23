/**
 * Reverses the order of elements in an array.
 * @template T - The type of elements in the array.
 * @param {T[]} arr - The array to be reversed.
 * @returns {T[]} A new array with the elements in reverse order.
 */
export function reverseArray(arr) {
  return [...arr].reverse();
}

/**
 * Returns the first element of an array, or undefined if the array is empty.
 * @template T - The type of elements in the array.
 * @param {T[]} arr - The array to get the first element from.
 * @returns {T | undefined} The first element of the array, or undefined.
 */
export function getFirstElement(arr) {
  return arr.length > 0 ? arr[0] : undefined;
}
