# user_resource_uris.md

This document illustrates good and bad practices for designing URIs for user-related resources in a RESTful API.

## Good URI Design Examples

-   **Collection of Users:**
    -   `GET /users`
    -   `POST /users`

-   **Specific User Resource:**
    -   `GET /users/{id}`
    -   `PUT /users/{id}`
    -   `PATCH /users/{id}`
    -   `DELETE /users/{id}`

-   **Sub-collection (Orders belonging to a User):**
    -   `GET /users/{id}/orders`
    -   `POST /users/{id}/orders`

-   **Specific Order of a User:**
    -   `GET /users/{user_id}/orders/{order_id}`

-   **User Profile (often a singleton resource for the authenticated user):**
    -   `GET /profile` (if context implies current user)
    -   `GET /users/{id}/profile`

-   **Searching Users:**
    -   `GET /users?search=john&status=active`

## Bad URI Design Examples

-   **Using Verbs in URIs:**
    -   `GET /getAllUsers` (Instead of `GET /users`)
    -   `POST /createNewUser` (Instead of `POST /users`)
    -   `PUT /updateUser` (Instead of `PUT /users/{id}`)
    -   `DELETE /deleteUser/{id}` (Instead of `DELETE /users/{id}`)

-   **Inconsistent Naming:**
    -   `GET /user` (for collection, should be plural `users`)
    -   `GET /products/{product_id}/user` (if it means the user who created the product, better to link or embed)

-   **Using Query Parameters for Resource Identification:**
    -   `GET /users?id=123` (Instead of `GET /users/123`)

-   **Exposing Implementation Details:**
    -   `GET /users/v1/get_user_data` (Mixing versioning and verbs, exposing internal function names)

-   **Deeply Nested and Unnecessary Complexity:**
    -   `GET /users/{id}/profile/details/contact-information` (Can often be flattened or handled with query parameters for specific fields)

## Key Takeaways

-   **Resources are Nouns:** Always think of your API endpoints as resources, which are nouns.
-   **Use Plural Nouns for Collections:** `/users`, `/products`.
-   **Use HTTP Methods for Actions:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE` define what you do with the resource.
-   **Keep URIs Clean and Predictable:** Easy to understand and remember.
-   **Hierarchical for Relationships:** Reflect parent-child relationships clearly.
