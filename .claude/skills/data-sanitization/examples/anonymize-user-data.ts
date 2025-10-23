
interface UserData {
  id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  ssn?: string;
  // Add other sensitive fields as needed
}

/**
 * Anonymizes sensitive user data for non-production environments.
 * Applies various techniques like hashing, masking, and substitution.
 * @param data The user data object to anonymize.
 * @returns An anonymized user data object.
 */
export function anonymizeUserData(data: UserData): UserData {
  const anonymizedData = { ...data };

  // Anonymize name: Replace with a generic placeholder or hash
  anonymizedData.name = `User ${data.id.substring(0, 8)}`;

  // Anonymize email: Replace username with a hash and use a generic domain
  const [username, domain] = anonymizedData.email.split('@');
  anonymizedData.email = `${hashString(username)}@example.com`;

  // Anonymize phone number: Mask all but last four digits
  anonymizedData.phone = `XXX-XXX-${data.phone.slice(-4)}`;

  // Anonymize address: Replace with a generic address or hash
  anonymizedData.address = `Anonymized Address for User ${data.id.substring(0, 8)}`;

  // Anonymize SSN: Mask all but last four digits if present
  if (anonymizedData.ssn) {
    anonymizedData.ssn = `XXX-XX-${data.ssn.slice(-4)}`;
  }

  // Add more anonymization rules for other sensitive fields

  return anonymizedData;
}

/**
 * Simple hashing function for demonstration purposes.
 * In a real application, use a cryptographically secure hashing algorithm.
 * @param str The string to hash.
 * @returns A simple hash of the string.
 */
function hashString(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash).toString(16);
}

// Example Usage:
// const sensitiveUser: UserData = {
//   id: "user-123",
//   name: "Alice Wonderland",
//   email: "alice.w@example.com",
//   phone: "123-456-7890",
//   address: "123 Rabbit Hole, Wonderland",
//   ssn: "987-65-4321",
// };

// const anonymizedUser = anonymizeUserData(sensitiveUser);
// console.log("Original:", sensitiveUser);
// console.log("Anonymized:", anonymizedUser);
