// bad-duplication.ts
// user-service.ts
interface User {
    id: string;
    name: string;
    email: string;
    role: "user" | "admin";
}

function getUserDetails(userId: string): User {
    // In a real application, this would fetch from a database or API
    const user: User = { id: userId, name: "John Doe", email: "john@example.com", role: "user" };
    if (user.role === "admin") {
        console.log(`Admin user ${user.name} logged in.`);
        // ... admin specific logic
    }
    return user;
}

// admin-service.ts
function getAdminDetails(adminId: string): User {
    // In a real application, this would fetch from a database or API
    const admin: User = { id: adminId, name: "Jane Smith", email: "jane@example.com", role: "admin" };
    if (admin.role === "admin") {
        console.log(`Admin user ${admin.name} logged in.`);
        // ... admin specific logic (identical to above)
    }
    return admin;
}

// Another example of duplication
function calculateDiscountedPrice(price: number, discountPercentage: number): number {
    if (discountPercentage > 1) {
        discountPercentage /= 100; // Assume percentage if > 1
    }
    return price * (1 - discountPercentage);
}

function applyCoupon(originalPrice: number, couponCode: string): number {
    let discount = 0;
    if (couponCode === "SUMMER20") {
        discount = 0.20; // 20% off
    } else if (couponCode === "SAVE10") {
        discount = 0.10; // 10% off
    }
    // Duplicated discount calculation logic
    return originalPrice * (1 - discount);
}

console.log("Bad Duplication Examples:");
console.log("User details:", getUserDetails("123"));
console.log("Admin details:", getAdminDetails("456"));
console.log("Discounted price:", calculateDiscountedPrice(100, 25));
console.log("Price with coupon:", applyCoupon(100, "SUMMER20"));
