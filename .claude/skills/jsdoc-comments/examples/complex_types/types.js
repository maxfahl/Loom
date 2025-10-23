/**
 * @typedef {object} UserProfile
 * @property {string} id - The user's unique identifier.
 * @property {string} username - The user's chosen username.
 * @property {string} email - The user's email address.
 * @property {string[]} roles - An array of roles assigned to the user.
 * @property {boolean} isActive - Indicates if the user account is active.
 * @property {Date} createdAt - The date and time when the user account was created.
 */

/** @type {UserProfile} */
export const defaultUser = {
  id: "usr_123",
  username: "guest",
  email: "guest@example.com",
  roles: ["viewer"],
  isActive: true,
  createdAt: new Date(),
};

/**
 * @typedef {object} ProductItem
 * @property {string} productId - The ID of the product.
 * @property {number} quantity - The quantity of the product.
 * @property {number} price - The price per unit of the product.
 */

/**
 * @typedef {object} Order
 * @property {string} orderId - Unique order identifier.
 * @property {string} userId - The ID of the user who placed the order.
 * @property {ProductItem[]} items - An array of product items in the order.
 * @property {number} totalAmount - The total amount of the order.
 * @property {'pending' | 'completed' | 'cancelled'} status - The current status of the order.
 */

/** @type {Order} */
export const exampleOrder = {
  orderId: "ord_456",
  userId: "usr_123",
  items: [
    { productId: "prod_A", quantity: 2, price: 10.50 },
    { productId: "prod_B", quantity: 1, price: 25.00 },
  ],
  totalAmount: 46.00,
  status: "pending",
};
