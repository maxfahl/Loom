---
name: java-spring-framework
version: 1.0.0
category: Backend / Java
tags: Java, Spring, Spring Boot, Microservices, REST API, JPA, Security, Cloud
description: Guides Claude in developing robust, scalable, and secure applications using the Java Spring Framework, focusing on modern Spring Boot 3.x best practices.
---

# Java Spring Framework Skill

## Skill Purpose

This skill enables Claude to assist developers in building high-quality, performant, and secure backend applications using the Java Spring Framework, particularly Spring Boot 3.x. It provides guidance on architectural patterns, data access, security, testing, and deployment, ensuring adherence to modern best practices and addressing common development challenges.

## When to Activate This Skill

Activate this skill when the user's request involves:
- Developing or modifying Java backend applications.
- Working with Spring Boot, Spring MVC, Spring Data JPA, Spring Security, or Spring Cloud.
- Designing RESTful APIs or microservices in Java.
- Optimizing Spring application performance or startup time.
- Implementing security features in a Spring application.
- Troubleshooting common Spring-related issues (e.g., N+1 queries, configuration problems).
- Migrating older Spring applications to newer versions (e.g., Spring Boot 3.x, Java 17+).
- Generating boilerplate code for Spring components.

## Core Knowledge

Claude should be proficient in the following core concepts and technologies related to the Java Spring Framework:

### Spring Boot 3.x Fundamentals
- **Project Setup**: Using Spring Initializr, build tools (Maven/Gradle).
- **Auto-configuration**: Understanding how Spring Boot simplifies configuration.
- **Dependency Management**: `spring-boot-starter-*` dependencies.
- **Configuration**: `@ConfigurationProperties`, `application.properties`/`application.yml`, externalized configuration.
- **Logging**: SLF4J with Logback/Log4j2.
- **Testing**: `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`, JUnit 5, Mockito.
- **Observability**: Spring Boot Actuator, Micrometer, OpenTelemetry for metrics, health checks, tracing.
- **Modern Java Features**: Leveraging Java 17+ features, especially Java 21 Virtual Threads (Project Loom).
- **Performance**: Ahead-of-Time (AOT) compilation, GraalVM Native Images for faster startup and reduced memory footprint.

### Web Development (Spring MVC / Spring WebFlux)
- **RESTful API Design**: `@RestController`, `@RequestMapping`, `@GetMapping`, `@PostMapping`, etc.
- **Request/Response Handling**: `@RequestBody`, `@ResponseBody`, `ResponseEntity`.
- **Validation**: `@Valid`, Bean Validation API (Hibernate Validator).
- **Exception Handling**: `@ControllerAdvice`, `@RestControllerAdvice` for global error handling.
- **Asynchronous Programming**: `CompletableFuture`, Spring WebFlux (reactive programming).

### Data Access (Spring Data JPA / Hibernate)
- **Entities**: `@Entity`, `@Table`, `@Id`, `@GeneratedValue`, relationships (`@OneToMany`, `@ManyToOne`, etc.).
- **Repositories**: `JpaRepository`, custom repositories, `@Query` annotations.
- **Transactions**: `@Transactional`.
- **Lazy vs. Eager Loading**: `FetchType.LAZY`, `FetchType.EAGER`.
- **N+1 Query Problem**: Identification and mitigation using `@EntityGraph`, `JOIN FETCH`.
- **Pagination and Sorting**: `Pageable`, `Sort`.
- **Optimistic Locking**: `@Version`.
- **Soft Deletion**: Implementing logical deletion.
- **Connection Pooling**: HikariCP configuration.

### Spring Security
- **Authentication**: Form-based, Basic, OAuth2/OpenID Connect, JWT.
- **Authorization**: Role-Based Access Control (RBAC) with `@PreAuthorize`, `@PostAuthorize`, method-level security.
- **CSRF Protection**: Understanding and configuring.
- **CORS**: Cross-Origin Resource Sharing configuration.
- **Password Encoding**: `PasswordEncoder` (e.g., BCrypt).
- **Secure Headers**: Helmet-like configurations.
- **Secret Management**: Environment variables, Vault integration.

### Microservices with Spring Cloud
- **API Gateway**: Spring Cloud Gateway, Zuul.
- **Service Discovery**: Eureka, Consul.
- **Circuit Breaker**: Resilience4j, Hystrix (legacy).
- **Distributed Configuration**: Spring Cloud Config Server.
- **Load Balancing**: Ribbon (legacy), Spring Cloud LoadBalancer.
- **Distributed Tracing**: Sleuth, OpenTelemetry.
- **Event-Driven Architecture**: Spring Cloud Stream, Kafka, RabbitMQ.

## Key Guidance for Claude

### ✅ Always Recommend
- **DTOs for API Responses**: Always map JPA entities to Data Transfer Objects (DTOs) before sending them as API responses to prevent exposing internal data structures and sensitive information.
- **Leverage Spring Boot Starters**: Use appropriate `spring-boot-starter-*` dependencies to quickly set up common functionalities.
- **Externalized Configuration**: Store sensitive data and environment-specific configurations outside the codebase (e.g., `application.yml`, environment variables, Spring Cloud Config).
- **Type-Safe Configuration**: Prefer `@ConfigurationProperties` for binding configuration properties over `@Value` for better type safety and testability.
- **Global Exception Handling**: Implement `@RestControllerAdvice` to centralize exception handling and provide consistent, user-friendly error responses.
- **Observability**: Integrate Spring Boot Actuator, Micrometer, and OpenTelemetry for comprehensive monitoring, metrics, and distributed tracing.
- **Modern Java & Spring Features**: Utilize Java 21 Virtual Threads for high concurrency and AOT compilation/GraalVM Native Images for optimized startup and memory footprint in Spring Boot 3.x.
- **HTTPS Everywhere**: Enforce HTTPS/TLS for all communication, especially for production environments.
- **CSRF Protection**: Keep Spring Security's CSRF protection enabled by default for state-changing operations.
- **Strong Authentication & Authorization**: Use OAuth2/OpenID Connect for authentication and implement fine-grained RBAC with `@PreAuthorize`.
- **Input Validation**: Validate all incoming request data using Bean Validation API (`@Valid`).
- **Connection Pooling**: Configure and use a robust connection pool like HikariCP for database interactions.
- **Soft Deletion**: For data that needs to be retained for auditing or recovery, implement soft delete mechanisms.
- **Modular Design**: Structure applications into logical modules, especially for microservices, to improve maintainability and scalability.

### ❌ Never Recommend
- **Exposing JPA Entities Directly**: Never return JPA entities directly from REST API endpoints. This can lead to N+1 problems, expose sensitive data, and create tight coupling.
- **Disabling CSRF Protection**: Do not disable CSRF protection in production environments unless there's a very specific, well-understood reason (e.g., stateless APIs using JWT where CSRF is handled differently).
- **Hardcoding Secrets**: Never hardcode API keys, database credentials, or other sensitive information directly in the code.
- **Ignoring N+1 Query Problem**: Do not ignore the N+1 query problem; it's a major performance killer. Actively identify and fix it.
- **Using `@Autowired` on Fields**: Prefer constructor injection for `@Autowired` dependencies to improve testability and immutability.
- **Catching `Exception` broadly**: Avoid catching generic `Exception` without specific handling; catch more specific exceptions.
- **Blocking I/O in Reactive Stacks**: In Spring WebFlux, avoid blocking I/O operations (e.g., traditional JPA calls) as it defeats the purpose of reactive programming.
- **Physical Deletion of Critical Data**: Avoid physically deleting data that might be needed for auditing, recovery, or historical analysis. Use soft deletion instead.

### Common Questions & Responses

**Q: How can I improve the startup time and reduce memory usage of my Spring Boot application?**
A: Leverage Spring Boot 3.x's support for GraalVM Native Images and Ahead-of-Time (AOT) compilation. This compiles your application into a native executable, significantly reducing startup time and memory footprint. Also, ensure you're using a recent Java version (e.g., Java 21) and consider optimizing your dependency tree.

**Q: What's the best way to handle N+1 query problems in Spring Data JPA?**
A: Identify the problematic queries using SQL logging. Then, use `@EntityGraph` on your repository methods for specific use cases, or write custom `@Query` methods with `JOIN FETCH` clauses to eagerly load associated entities in a single query.

**Q: How do I secure my Spring Boot REST API?**
A: Implement Spring Security. Use OAuth2/OpenID Connect for authentication, configure JWTs for stateless APIs (with short-lived access tokens and refresh tokens), enforce HTTPS, enable CSRF protection, and implement method-level authorization using `@PreAuthorize` for fine-grained access control. Always validate input and manage secrets securely.

**Q: When should I use DTOs, and why are they important?**
A: Always use DTOs when transferring data between layers (e.g., from service to controller, or as API request/response bodies). They are crucial for:
1.  **Decoupling**: Separating your domain model (JPA entities) from your API contract.
2.  **Security**: Preventing exposure of sensitive internal fields.
3.  **Performance**: Sending only necessary data over the wire.
4.  **Flexibility**: Allowing changes to the internal model without affecting the API.

**Q: How can I make my Spring Boot application more observable?**
A: Integrate Spring Boot Actuator for health endpoints and metrics. Use Micrometer to expose custom metrics to monitoring systems like Prometheus. Implement distributed tracing with OpenTelemetry (integrated via Spring Cloud Sleuth) to track requests across microservices. Centralize logs with tools like ELK stack or Grafana Loki.

## Anti-Patterns to Flag

### ❌ Anti-Pattern: Exposing JPA Entities Directly in REST APIs
```java
// BAD: Directly returning JPA entity
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserRepository userRepository;

    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String passwordHash; // Sensitive data exposed!
    private String email;
    // ... other fields, potentially with lazy-loaded collections
}
```
**Why it's bad**: Exposes sensitive fields (`passwordHash`), can lead to N+1 problems if lazy-loaded collections are accessed outside a transaction, and tightly couples the API to the database schema.

### ✅ Good Practice: Using DTOs
```java
// GOOD: Using a DTO for API response
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserService userService; // Service layer handles mapping

    @GetMapping("/{id}")
    public UserResponseDto getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }
}

// DTO for API response
public class UserResponseDto {
    private Long id;
    private String username;
    private String email;
    // No passwordHash or other sensitive internal fields
    // No lazy-loaded collections directly exposed
}

// Service layer responsible for mapping
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public UserResponseDto getUserById(Long id) {
        User user = userRepository.findById(id).orElseThrow(() -> new UserNotFoundException("User not found"));
        // Map entity to DTO
        UserResponseDto dto = new UserResponseDto();
        dto.setId(user.getId());
        dto.setUsername(user.getUsername());
        dto.setEmail(user.getEmail());
        return dto;
    }
}
```

### ❌ Anti-Pattern: N+1 Query Problem
```java
// BAD: N+1 Query Problem
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    // Imagine Order has a @OneToMany relationship with OrderItem
    // When fetching all orders, then iterating to access order items,
    // a separate query is executed for each order's items.
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    public List<Order> getAllOrdersWithItems() {
        List<Order> orders = orderRepository.findAll(); // Fetches N orders
        for (Order order : orders) {
            order.getOrderItems().size(); // N separate queries for items
        }
        return orders;
    }
}
```
**Why it's bad**: Leads to a large number of database queries (1 for orders + N for each order's items), severely impacting performance.

### ✅ Good Practice: Mitigating N+1 with `JOIN FETCH` or `@EntityGraph`
```java
// GOOD: Mitigating N+1 with JOIN FETCH
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("SELECT o FROM Order o JOIN FETCH o.orderItems")
    List<Order> findAllWithOrderItems();

    @EntityGraph(attributePaths = "orderItems")
    List<Order> findAll(); // Overrides default findAll to use entity graph
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    public List<Order> getAllOrdersWithItemsOptimized() {
        return orderRepository.findAllWithOrderItems(); // Fetches all orders and their items in 1-2 queries
    }
}
```

### ❌ Anti-Pattern: Hardcoding Secrets
```java
// BAD: Hardcoding database credentials
@Configuration
public class DataSourceConfig {
    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName("org.postgresql.Driver");
        dataSource.setUrl("jdbc:postgresql://localhost:5432/mydb");
        dataSource.setUsername("admin"); // Hardcoded!
        dataSource.setPassword("mysecretpassword"); // Hardcoded!
        return dataSource;
    }
}
```
**Why it's bad**: Security risk, difficult to manage across environments, and requires code changes for credential updates.

### ✅ Good Practice: Using Externalized Configuration
```java
// GOOD: Using externalized configuration (application.yml or environment variables)
@Configuration
public class DataSourceConfig {
    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource dataSource() {
        return DataSourceBuilder.create().build();
    }
}
// application.yml
// spring:
//   datasource:
//     url: jdbc:postgresql://localhost:5432/mydb
//     username: ${DB_USERNAME} # Injected from environment variable
//     password: ${DB_PASSWORD} # Injected from environment variable
```

## Code Review Checklist

When reviewing Spring Framework code, ensure the following:

- [ ] **DTO Usage**: Are DTOs used for all API request/response bodies, separating domain models from API contracts?
- [ ] **Configuration**: Are `@ConfigurationProperties` used for type-safe configuration? Are sensitive configurations externalized (environment variables, config server)?
- [ ] **Exception Handling**: Is `@RestControllerAdvice` implemented for consistent global exception handling?
- [ ] **Observability**: Are Actuator endpoints configured and secured? Is Micrometer used for custom metrics? Is OpenTelemetry integrated for tracing?
- [ ] **Performance**: Are N+1 query problems mitigated using `JOIN FETCH` or `@EntityGraph`? Is pagination implemented for large datasets? Is HikariCP configured?
- [ ] **Security**: Is HTTPS enforced? Is CSRF protection enabled for state-changing operations? Are passwords securely encoded (e.g., BCrypt)? Is input validated? Are secrets managed securely (no hardcoding)?
- [ ] **Transactions**: Are `@Transactional` annotations used correctly and on appropriate service methods?
- [ ] **Dependency Injection**: Is constructor injection preferred over field injection for `@Autowired`?
- [ ] **Logging**: Is logging configured appropriately (e.g., SLF4J)? Are sensitive data not logged?
- [ ] **Testing**: Are unit, integration, and slice tests written using JUnit 5, Mockito, and Spring Boot testing utilities?
- [ ] **Modern Java**: If applicable, are Java 17+ features (e.g., records, sealed classes) and Java 21 Virtual Threads utilized effectively?
- [ ] **Native Image Compatibility**: If targeting GraalVM Native Images, is the application compatible and configured correctly?
- [ ] **Code Quality**: Adherence to SOLID principles, clean code, and project-specific coding standards.

## Related Skills

- **Containerization (Docker)**: For packaging and deploying Spring Boot applications.
- **CI/CD (GitHub Actions)**: For automating build, test, and deployment pipelines for Spring projects.
- **Database Migration Management**: For managing database schema changes (e.g., Flyway, Liquibase).
- **REST API Design**: For general principles of designing effective RESTful APIs.
- **TypeScript Strict Mode**: For frontend development that might consume Spring APIs.
- **Automated Test Generation**: For generating test boilerplate for Spring components.

## Examples Directory Structure

```
examples/
├── rest-api/
│   ├── src/main/java/com/example/demo/controller/UserController.java
│   ├── src/main/java/com/example/demo/service/UserService.java
│   ├── src/main/java/com/example/demo/repository/UserRepository.java
│   ├── src/main/java/com/example/demo/model/User.java
│   ├── src/main/java/com/example/demo/dto/UserResponseDto.java
│   └── src/main/resources/application.yml
├── jpa-entity-relationships/
│   ├── src/main/java/com/example/demo/model/Order.java
│   ├── src/main/java/com/example/demo/model/OrderItem.java
│   ├── src/main/java/com/example/demo/repository/OrderRepository.java
│   └── src/main/java/com/example/demo/service/OrderService.java
├── spring-security-jwt/
│   ├── src/main/java/com/example/demo/config/SecurityConfig.java
│   ├── src/main/java/com/example/demo/filter/JwtAuthenticationFilter.java
│   ├── src/main/java/com/example/demo/service/JwtService.java
│   └── src/main/java/com/example/demo/controller/AuthController.java
└── native-image-config/
    └── src/main/resources/META-INF/native-image/reflect-config.json
```

## Custom Scripts Section

For the Java Spring Framework skill, the following automation scripts address common pain points and enhance developer productivity:

1.  **`spring-project-initializer.sh`**: Automates the creation of a new Spring Boot project with best-practice configurations, including chosen dependencies, Java version, and initial project structure.
2.  **`jpa-dto-generator.py`**: Generates DTOs and basic mappers from existing JPA entities, reducing boilerplate and enforcing API-entity separation.
3.  **`nplus1-detector.sh`**: A shell script that analyzes application logs to detect potential N+1 query problems by looking for repetitive query patterns.
4.  **`spring-security-config-auditor.py`**: Audits a Spring Security configuration file for common misconfigurations and adherence to best practices (e.g., CSRF, HTTPS, password encoders).
5.  **`native-image-preparer.sh`**: Prepares a Spring Boot project for GraalVM Native Image compilation by adding necessary build plugins and suggesting common reflection/resource configurations.
