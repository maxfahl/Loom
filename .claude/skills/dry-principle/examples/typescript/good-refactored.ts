// good-refactored.ts
// utils/types.ts
interface User {
    id: string;
    name: string;
    email: string;
    role: "user" | "admin";
}

// utils/auth.ts
function logAdminActivity(user: User): void {
    if (user.role === "admin") {
        console.log(`Admin user ${user.name} logged in.`);
        // ... admin specific logic
    }
}

// user-service.ts
function getUserDetails(userId: string): User {
    // In a real application, this would fetch from a database or API
    const user: User = { id: userId, name: "John Doe", email: "john@example.com", role: "user" };
    logAdminActivity(user); // Reused logic
    return user;
}

// admin-service.ts
function getAdminDetails(adminId: string): User {
    // In a real application, this would fetch from a database or API
    const admin: User = { id: adminId, name: "Jane Smith", email: "jane@example.com", role: "admin" };
    logAdminActivity(admin); // Reused logic
    return admin;
}

// utils/pricing.ts
function calculateFinalPrice(price: number, discountPercentage: number): number {
    if (discountPercentage > 1) {
        discountPercentage /= 100; // Assume percentage if > 1
    }
    return price * (1 - discountPercentage);
}

// product-service.ts
function getProductPrice(basePrice: number, promoCode?: string): number {
    let discount = 0;
    if (promoCode === "SUMMER20") {
        discount = 0.20; // 20% off
    } else if (promoCode === "SAVE10") {
        discount = 0.10; // 10% off
    }
    return calculateFinalPrice(basePrice, discount);
}

console.log("Good Refactored Examples:");
const user1: User = getUserDetails("123");
const admin1: User = getAdminDetails("456");
console.log("User details:", user1);
console.log("Admin details:", admin1);
console.log("Product price with promo:", getProductPrice(100, "SUMMER20"));
console.log("Product price without promo:", getProductPrice(100));
