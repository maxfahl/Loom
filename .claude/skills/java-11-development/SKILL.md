---
name: java-11-development
version: 1.0.0
category: Backend Development / Java
tags: Java, Java 11, JDK 11, Backend, JVM, Spring Boot, Maven, Gradle
description: Provides comprehensive guidance for developing applications with Java 11, including best practices, modern features, and common pitfalls.
---

# Java 11 Development Skill

## 1. Skill Purpose

This skill enables Claude to effectively assist with Java 11 application development. It covers core language features, modern development practices, build tool usage (Maven/Gradle), testing strategies, and common pitfalls to ensure robust, maintainable, and performant Java applications.

## 2. When to Activate This Skill

Activate this skill when the user's request involves:
- Developing new Java applications or features using Java 11.
- Refactoring existing Java 11 codebase.
- Troubleshooting Java 11 specific issues (e.g., module system, new API usage).
- Setting up Java 11 projects with Maven or Gradle.
- Writing unit or integration tests for Java 11 applications.
- Discussing Java 11 best practices, performance, or security.
- Migrating from older Java versions to Java 11.

## 3. Core Knowledge

Claude should be familiar with:

### Java 11 Language Features
- **Local-Variable Syntax for Lambda Parameters (var):**
  ```java
  (var firstName, var lastName) -> firstName + lastName
  ```
- **HTTP Client (java.net.http):** New standard HTTP client API.
  ```java
  HttpClient client = HttpClient.newHttpClient();
  HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://example.com"))
        .build();
  client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
        .thenApply(HttpResponse::body)
        .thenAccept(System.out::println);
  ```
- **Nest-Based Access Control:** Enhancements to nested classes.
- **Dynamic Class-File Constants (JEP 309).**
- **Epsilon Garbage Collector (JEP 318):** A no-op garbage collector for performance testing.
- **ZGC (JEP 333):** A scalable low-latency garbage collector (experimental in Java 11).
- **Flight Recorder (JEP 328) and Mission Control (JEP 349):** Tools for profiling and monitoring.
- **Removed Java EE and CORBA Modules:** Awareness of removed modules and potential migration impact.

### Modern Java Development Practices
- **Immutability:** Favoring immutable objects to simplify concurrency and reduce side effects.
- **Functional Programming:** Leveraging `java.util.function` interfaces, Streams API, and Lambda expressions for concise and expressive code.
- **Optional API:** Using `java.util.Optional` to handle null values gracefully and prevent `NullPointerException`.
- **Try-with-resources:** Ensuring proper resource management for I/O operations and database connections.
- **Dependency Injection:** Understanding frameworks like Spring for managing component dependencies.
- **Logging:** Using SLF4J with Logback or Log4j2 for effective logging.

### Build Tools
- **Maven:** `pom.xml` structure, dependency management, plugins, build lifecycle.
- **Gradle:** `build.gradle` (Groovy/Kotlin DSL), task management, dependency management.

### Testing Frameworks
- **JUnit 5:** `@Test`, `@BeforeEach`, `@AfterEach`, `@DisplayName`, assertions.
- **Mockito:** `@Mock`, `@InjectMocks`, `when().thenReturn()`, `verify()`.
- **Spring Test (for Spring Boot applications):** `@SpringBootTest`, `@WebMvcTest`.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ **Use `var` for local variables** where the type is obvious to improve readability and reduce boilerplate.
- ✅ **Leverage the new HTTP Client API** (`java.net.http`) for modern, non-blocking HTTP communication.
- ✅ **Employ `Optional`** to explicitly handle the absence of values, making code safer and more readable.
- ✅ **Utilize `try-with-resources`** for all resources that implement `AutoCloseable` to prevent resource leaks.
- ✅ **Write comprehensive unit and integration tests** using JUnit 5 and Mockito.
- ✅ **Prefer immutable objects** where possible to simplify concurrency and reasoning about state.
- ✅ **Use Streams API and Lambda expressions** for collection processing and functional programming paradigms.
- ✅ **Follow established logging best practices** (e.g., using SLF4J with Logback) and log at appropriate levels.
- ✅ **Choose Maven or Gradle** for project management and dependency resolution. Gradle is often preferred for its flexibility and performance in larger projects.
- ✅ **Adhere to Java coding conventions** (e.g., Google Java Format, Oracle Code Conventions).

### Never Recommend (❌ anti-patterns)
- ❌ **Avoid `NullPointerException` by not checking for nulls.** Always assume inputs can be null unless explicitly guaranteed otherwise, or use `Optional`.
- ❌ **Never use `==` for String comparison.** Always use `equals()` or `equalsIgnoreCase()`.
- ❌ **Do not use empty `catch` blocks.** Always handle exceptions gracefully, log them, or rethrow them.
- ❌ **Avoid excessive use of `System.out.println()` for logging.** Use a proper logging framework.
- ❌ **Do not concatenate strings in loops using `+` operator.** Use `StringBuilder` for efficiency.
- ❌ **Avoid modifying collections while iterating over them** without using the iterator's `remove()` method, to prevent `ConcurrentModificationException`.
- ❌ **Do not ignore compiler warnings.** Treat warnings as errors and address them.
- ❌ **Avoid using deprecated APIs.** Always look for modern alternatives.

### Common Questions & Responses

- **Q: How do I handle `NullPointerException` in Java 11?**
  - **A:** Use `java.util.Optional` for values that might be absent. For example, `Optional.ofNullable(value).ifPresent(v -> /* use v */);` or `value.orElse(defaultValue);`. Also, perform explicit null checks where `Optional` is not applicable.

- **Q: What's the best way to make HTTP calls in Java 11?**
  - **A:** Use the built-in `java.net.http.HttpClient`. It supports both synchronous and asynchronous operations and is designed for modern web protocols.

- **Q: Should I use Maven or Gradle for my new Java 11 project?**
  - **A:** Both are excellent. For simpler projects or if you prefer convention over configuration, Maven is a solid choice. For more complex projects, multi-module builds, or if you need more flexibility and performance, Gradle (especially with Kotlin DSL) is often preferred.

- **Q: How can I ensure my resources are closed properly?**
  - **A:** Always use the `try-with-resources` statement for any resource that implements `AutoCloseable`, such as `InputStream`, `OutputStream`, `Reader`, `Writer`, `Connection`, `Statement`, `ResultSet`.

## 5. Anti-Patterns to Flag

### Bad vs. Good: String Concatenation in Loops
```java
// BAD: Inefficient string concatenation in a loop
String result = "";
for (int i = 0; i < 1000; i++) {
    result += "Number: " + i;
}

// GOOD: Efficient string concatenation using StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append("Number: ").append(i);
}
String efficientResult = sb.toString();
```

### Bad vs. Good: Null Handling
```java
// BAD: Prone to NullPointerException
public String getUserName(User user) {
    return user.getName(); // What if user is null?
}

// GOOD: Using Optional for safe null handling
public Optional<String> getUserNameSafe(User user) {
    return Optional.ofNullable(user)
                   .map(User::getName);
}

// Usage:
// getUserNameSafe(user).ifPresent(name -> System.out.println(name));
// String name = getUserNameSafe(user).orElse("Guest");
```

### Bad vs. Good: Resource Management
```java
// BAD: Resource leak if an exception occurs
public void readFileBad(String filePath) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(filePath));
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
    reader.close(); // Might not be called
}

// GOOD: Automatic resource management with try-with-resources
public void readFileGood(String filePath) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
    } // reader is automatically closed here
}
```

## 6. Code Review Checklist

- [ ] Are `Optional` and `try-with-resources` used appropriately?
- [ ] Is the new HTTP Client (`java.net.http`) used for modern HTTP communication?
- [ ] Are `var` keywords used judiciously for local variables where type inference improves readability?
- [ ] Are `equals()` and `hashCode()` correctly overridden for custom objects?
- [ ] Is logging implemented using a proper framework (e.g., SLF4J) instead of `System.out.println()`?
- [ ] Are unit and integration tests present and comprehensive (JUnit 5, Mockito)?
- [ ] Is the code free from `NullPointerException` risks?
- [ ] Are String concatenations in loops handled efficiently with `StringBuilder`?
- [ ] Are dependencies managed correctly with Maven or Gradle?
- [ ] Does the code adhere to Java 11 coding conventions and best practices?
- [ ] Are there any deprecated APIs being used? If so, are there plans to migrate?

## 7. Related Skills

- `spring-boot-development`: For building web applications and microservices.
- `maven-project-management`: For advanced Maven usage.
- `gradle-project-management`: For advanced Gradle usage.
- `junit-mockito-testing`: For in-depth testing strategies.
- `docker-containerization`: For containerizing Java applications.

## 8. Examples Directory Structure

```
examples/
├── HelloWorld.java             # Basic "Hello, World!" application
├── HttpClientExample.java      # Demonstrates new HTTP Client usage
├── OptionalExample.java        # Shows proper Optional usage
├── StreamApiExample.java       # Examples of Streams and Lambdas
├── User.java                   # Simple POJO for examples
└── UserServiceTest.java        # JUnit 5 and Mockito example
```

## 9. Custom Scripts Section

For Java 11 development, the following scripts would significantly improve developer productivity:

1.  **`new-java-project.sh`**: A shell script to bootstrap a new Java 11 project using Maven or Gradle, including basic project structure and a `Main` class.
2.  **`run-java-app.sh`**: A shell script to compile and run a single Java class or a full Maven/Gradle project.
3.  **`java-code-quality.sh`**: A shell script to run common code quality checks (Maven/Gradle build, tests, and optionally static analysis tools like Checkstyle/SpotBugs if configured).
4.  **`update-java-dependencies.py`**: A Python script to check for and update outdated Maven/Gradle dependencies.
