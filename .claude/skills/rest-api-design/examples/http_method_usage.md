# http_method_usage.md

This document outlines the correct and idiomatic usage of standard HTTP methods (verbs) in RESTful API design.

## GET Method

-   **Purpose**: Retrieve a representation of a resource or a collection of resources.
-   **Characteristics**:
    -   **Safe**: Should not cause any side effects on the server (i.e., it should not change the state of the server).
    -   **Idempotent**: Making the same GET request multiple times will yield the same result (the resource state remains unchanged).
    -   **Cacheable**: Responses can be cached by clients or intermediaries.
-   **Usage Examples**:
    -   `GET /users`: Retrieve a list of all users.
    -   `GET /users/{id}`: Retrieve a specific user by ID.
    -   `GET /users/{id}/orders`: Retrieve all orders for a specific user.
    -   `GET /products?category=electronics&sort=price`: Retrieve filtered and sorted products.

## POST Method

-   **Purpose**: Create a new resource or submit data to be processed.
-   **Characteristics**:
    -   **Not Safe**: Typically causes side effects on the server (e.g., creates a new record).
    -   **Not Idempotent**: Making the same POST request multiple times will likely create multiple resources or have different effects.
    -   **Not Cacheable**: Responses are generally not cached.
-   **Usage Examples**:
    -   `POST /users`: Create a new user.
    -   `POST /products/{id}/reviews`: Add a new review to a product.
    -   `POST /login`: Submit credentials for authentication.

## PUT Method

-   **Purpose**: Update an existing resource completely, or create a resource if it does not exist at the specified URI.
-   **Characteristics**:
    -   **Not Safe**: Modifies the state of the server.
    -   **Idempotent**: Making the same PUT request multiple times will result in the same resource state (the resource is replaced with the same data each time).
    -   **Not Cacheable**: Responses are generally not cached.
-   **Usage Examples**:
    -   `PUT /users/{id}`: Replace the entire user resource with the data provided in the request body.
    -   `PUT /products/{id}`: Replace the entire product resource.

## PATCH Method

-   **Purpose**: Partially update an existing resource.
-   **Characteristics**:
    -   **Not Safe**: Modifies the state of the server.
    -   **Not Idempotent**: Making the same PATCH request multiple times might have different results if the patch operation is not designed to be idempotent (e.g., incrementing a counter).
    -   **Not Cacheable**: Responses are generally not cached.
-   **Usage Examples**:
    -   `PATCH /users/{id}`: Update only the `email` field of a user, leaving other fields unchanged.
    -   `PATCH /products/{id}`: Update only the `price` and `stock` of a product.

## DELETE Method

-   **Purpose**: Remove a resource identified by its URI.
-   **Characteristics**:
    -   **Not Safe**: Causes side effects on the server (deletes a resource).
    -   **Idempotent**: Making the same DELETE request multiple times will result in the same resource state (the resource is either deleted or remains deleted).
    -   **Not Cacheable**: Responses are generally not cached.
-   **Usage Examples**:
    -   `DELETE /users/{id}`: Delete a specific user by ID.
    -   `DELETE /products/{id}`: Delete a specific product.

## HEAD Method

-   **Purpose**: Identical to GET, but without the response body. Used to retrieve metadata (headers) about a resource.
-   **Characteristics**: Safe, Idempotent, Cacheable.
-   **Usage Examples**:
    -   `HEAD /users/{id}`: Check if a user exists and retrieve its headers without downloading the full user data.

## OPTIONS Method

-   **Purpose**: Retrieve the communication options (HTTP methods) available for a resource.
-   **Characteristics**: Safe, Idempotent, Cacheable.
-   **Usage Examples**:
    -   `OPTIONS /users`: Discover which HTTP methods are supported for the `/users` endpoint (e.g., GET, POST).

## Key Considerations

-   **Consistency**: Always use HTTP methods consistently across your API.
-   **Semantics**: Understand the semantic meaning of each method and use it appropriately.
-   **Safety and Idempotence**: Design your API operations to respect the safety and idempotence properties of the HTTP methods.
