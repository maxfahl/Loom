// comments_why_not_what.ts

// BAD Example: Comments explaining the obvious 'what'

function calculateDiscount(price: number, quantity: number): number {
  // Calculate total price
  const total = price * quantity;
  // Apply 10% discount if total is over 100
  if (total > 100) {
    return total * 0.9;
  } else {
    // No discount
    return total;
  }
}

// GOOD Example: Comments explaining the 'why' or complex logic

const MIN_DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.10;

/**
 * Calculates the final price after applying a conditional discount.
 * @param price The unit price of the item.
 * @param quantity The number of items.
 * @returns The total price after discount.
 */
function calculateFinalPrice(price: number, quantity: number): number {
  const total = price * quantity;

  // Why: Apply a 10% discount only for orders exceeding a certain value
  // to encourage larger purchases, as per marketing strategy.
  if (total > MIN_DISCOUNT_THRESHOLD) {
    return total * (1 - DISCOUNT_RATE);
  }
  return total;
}

// Another GOOD Example: Explaining a workaround or non-obvious behavior

// Why: This specific regex is used to handle a known bug in older browser versions
// where standard URL parsing fails for certain international characters.
const legacyUrlRegex = /^(?:([A-Za-z]+):)?(\/\/(?:[^@:]*(?::[^@:]*)?@)?(?:[^\/?#:]*)(?::(\d+))?)?([^?#]*)(\?(?:[^#]*))?(?:#(.*))?$/;
