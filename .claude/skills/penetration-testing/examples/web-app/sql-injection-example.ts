/**
 * @file sql-injection-example.ts
 * @description TypeScript snippet showing a vulnerable SQL query and a parameterized query fix.
 *              This is for educational purposes only to show how SQL Injection can occur.
 *              DO NOT use vulnerable code in production.
 */

// --- Scenario: SQL Injection in a user lookup function ---
// Imagine a backend service that retrieves user information based on a user ID.

// --- BAD Example: Vulnerable SQL Query (Conceptual Node.js/Express with MySQL) ---
// This example assumes a Node.js backend using a library like 'mysql' or 'mysql2'
// where queries are constructed by concatenating user input directly.

function getVulnerableUser(userId: string): string {
    // In a real application, this would interact with a database.
    // For demonstration, we're just showing the query string.
    const query = `SELECT * FROM users WHERE id = '${userId}'`;
    console.log(`\n[BAD] Vulnerable Query: ${query}`);
    // If userId is '1' OR '1'='1', the query becomes:
    // SELECT * FROM users WHERE id = '1' OR '1'='1'
    // which returns all users.
    // If userId is '1; DROP TABLE users;', the query becomes:
    // SELECT * FROM users WHERE id = '1'; DROP TABLE users;'
    // which could delete the users table.
    return query;
}

// --- GOOD Example: Parameterized SQL Query (Conceptual Node.js/Express with MySQL) ---
// This example shows how to use parameterized queries to prevent SQL injection.
// The database driver handles the proper escaping of the user input.

function getSafeUser(userId: string): string {
    // In a real application, this would use a database client's parameterized query feature.
    // e.g., `connection.execute('SELECT * FROM users WHERE id = ?', [userId]);`
    const query = `SELECT * FROM users WHERE id = ?`;
    const params = [userId];
    console.log(`\n[GOOD] Safe Query: ${query}`);
    console.log(`[GOOD] Parameters: ${JSON.stringify(params)}`);
    // The database driver ensures that 'userId' is treated as a literal value,
    // not as executable SQL code.
    return `Query: ${query}, Params: ${JSON.stringify(params)}`;
}

// --- Demonstration ---
console.log("--- SQL Injection Examples ---");

// Vulnerable calls
getVulnerableUser("1");
getVulnerableUser("1' OR '1'='1"); // Injects 'OR '1'='1' to bypass authentication/retrieve all records
getVulnerableUser("1; DROP TABLE users;"); // Injects a second query to drop a table

// Safe calls
getSafeUser("1");
getSafeUser("1' OR '1'='1"); // The malicious input is treated as a string literal
getSafeUser("1; DROP TABLE users;"); // The malicious input is treated as a string literal

// --- Key Takeaway ---
// ALWAYS use parameterized queries or prepared statements when constructing SQL queries
// that include user-supplied input. Never concatenate user input directly into SQL strings.
