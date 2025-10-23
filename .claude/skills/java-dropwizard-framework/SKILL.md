--- 
Name: java-dropwizard-framework
Version: 1.0.0
Category: Backend / Java / Microservices
Tags: Java, DropWizard, REST, Microservices, API, Backend, Jetty, Jersey, Jackson
Description: Enables Claude to assist with building high-performance RESTful microservices using the DropWizard framework.
---


# Java DropWizard Framework Skill

## 1. Skill Purpose

This skill enables Claude to provide comprehensive guidance and assistance for developing, testing, and deploying high-performance RESTful microservices using the Java DropWizard framework. It covers core concepts, best practices, common patterns, and automation strategies to streamline the development lifecycle.

## 2. When to Activate This Skill

Activate this skill when the user is:
- Starting a new Java RESTful API project and considering DropWizard.
- Developing or maintaining an existing DropWizard application.
- Troubleshooting issues in a DropWizard service (e.g., configuration, performance, deployment).
- Looking for best practices in DropWizard application design, testing, or deployment.
- Seeking automation scripts for DropWizard project setup, testing, or CI/CD.

Keywords/Patterns: "DropWizard", "Java REST API", "microservice with DropWizard", "DropWizard configuration", "DropWizard testing", "DropWizard deployment", "Jetty", "Jersey", "Jackson for Java API".

## 3. Core Knowledge

Claude should understand the following fundamental concepts and components of DropWizard:

### 3.1. Architecture & Core Components
- **Embedded HTTP Server (Jetty)**: How DropWizard bundles Jetty for self-contained applications.
- **REST API Framework (Jersey)**: JAX-RS implementation for defining API endpoints.
- **JSON (De)serialization (Jackson)**: Automatic conversion between Java objects and JSON.
- **Configuration (YAML)**: Externalized configuration using YAML files and `io.dropwizard.Configuration`.
- **Metrics**: Integration with `Dropwizard Metrics` for application monitoring.
- **Logging (Logback with Slf4j)**: Flexible and efficient logging.
- **Health Checks**: Built-in mechanisms for monitoring service health.
- **Validation (Hibernate Validator)**: Declarative input/output validation.

### 3.2. Project Structure
- **Maven Archetype**: Standard way to bootstrap a DropWizard project.
- **Fat JAR**: Packaging the application and all dependencies into a single executable JAR.
- **Modular Structure**: `project-api` (models), `project-client` (client code), `project-application` (core service logic).

### 3.3. Key Classes and Concepts
- `io.dropwizard.Application`: The entry point of a DropWizard application.
- `io.dropwizard.Configuration`: Base class for application-specific configuration.
- `io.dropwizard.setup.Environment`: Provides access to Jetty, Jersey, Jackson, etc.
- `io.dropwizard.setup.Bootstrap`: Used for initial setup, bundles, and commands.
- Resources (JAX-RS annotated classes): Handle incoming HTTP requests.
- Representations (POJOs): Data transfer objects for JSON payloads.
- HealthCheck classes: Implement `com.codahale.metrics.health.HealthCheck`.

## 4. Key Guidance for Claude

### Always Recommend (✅ Best Practices)

- ✅ **Use Maven Archetypes for Project Setup**: Start new projects with `dropwizard-archetype` for a consistent and best-practice foundation.
- ✅ **Externalize Configuration**: Always use `config.yml` for environment-specific settings. Leverage environment variables for sensitive data or overrides.
- ✅ **Build Fat JARs**: Package applications as fat JARs for simplified deployment and portability.
- ✅ **Implement Health Checks**: Provide comprehensive health checks for all critical dependencies (database, external services, caches) to ensure operational readiness.
- ✅ **Monitor with Metrics**: Instrument critical code paths with `Dropwizard Metrics` to gain insights into application performance and identify bottlenecks.
- ✅ **Structured Logging**: Use SLF4J and Logback for structured, searchable logs. Configure log levels appropriately for different environments.
- ✅ **Input Validation**: Apply `Hibernate Validator` annotations to resource method parameters and representation classes to ensure data integrity.
- ✅ **Modular Project Structure**: For larger applications, consider separating API contracts, client code, and application logic into distinct Maven modules (`-api`, `-client`, `-application`).
- ✅ **Comprehensive Testing**: Utilize `dropwizard-testing` for unit, integration, and full-stack tests. Employ `Testcontainers` for realistic integration tests with external services.
- ✅ **Dockerize Applications**: Containerize DropWizard services using Docker for consistent environments and easier orchestration.
- ✅ **Leverage Modern Java Features**: Ensure compatibility with Java 17+ and explore virtual threads (Java 21+) for I/O-bound workloads, testing performance benefits.

### Never Recommend (❌ Anti-Patterns)

- ❌ **Hardcoding Configuration**: Avoid embedding configuration values directly in code.
- ❌ **Ignoring Health Checks**: Do not skip implementing health checks; they are crucial for production monitoring.
- ❌ **Manual Dependency Management**: Rely on Maven/Gradle for dependency management; avoid manually adding JARs.
- ❌ **Blocking I/O in Critical Paths without Virtual Threads**: Be mindful of blocking operations in high-throughput endpoints. If not using Java 21+ virtual threads, consider asynchronous patterns or ensure thread pool sizes are adequate.
- ❌ **Over-engineering Simple Services**: DropWizard is opinionated and lightweight. Avoid introducing unnecessary frameworks or complexities that negate its benefits.
- ❌ **Inadequate Logging**: Do not use `System.out.println` for logging. Ensure logs provide sufficient context for debugging.
- ❌ **Skipping Input Validation**: Never trust client input; always validate it.

### Common Questions & Responses (FAQ Format)

**Q: How do I start a new DropWizard project?**
A: Use the Maven archetype:
```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.dropwizard \
  -DarchetypeArtifactId=dropwizard-archetype \
  -DarchetypeVersion=5.0.0 \
  -DgroupId=com.example \
  -DartifactId=my-app \
  -Dversion=1.0.0-SNAPSHOT \
  -Dpackage=com.example.my_app
```
(Adjust `archetypeVersion` to the latest stable version, e.g., 5.0.0 for Java 17+).

**Q: How do I configure my DropWizard application?**
A: Create a `config.yml` file and a corresponding `Configuration` class that extends `io.dropwizard.Configuration`.
```yaml
# config.yml
server:
  applicationConnectors:
    - type: http
      port: 8080
  adminConnectors:
    - type: http
      port: 8081
template: Hello, %s!
defaultName: Stranger
```
```java
// src/main/java/com/example/my_app/MyAppConfiguration.java
package com.example.my_app;

import io.dropwizard.core.Configuration;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotEmpty;

public class MyAppConfiguration extends Configuration {
    @NotEmpty
    private String template;

    @NotEmpty
    private String defaultName;

    @JsonProperty
    public String getTemplate() {
        return template;
    }

    @JsonProperty
    public void setTemplate(String template) {
        this.template = template;
    }

    @JsonProperty
    public String getDefaultName() {
        return defaultName;
    }

    @JsonProperty
    public void setDefaultName(String defaultName) {
        this.defaultName = defaultName;
    }
}
```

**Q: How do I create a REST endpoint (Resource)?**
A: Create a Java class annotated with JAX-RS annotations.
```java
// src/main/java/com/example/my_app/resources/HelloWorldResource.java
package com.example.my_app.resources;

import com.example.my_app.api.Saying;
import com.example.my_app.MyAppConfiguration;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import java.util.concurrent.atomic.AtomicLong;
import java.util.Optional;

@Path("/hello-world")
@Produces(MediaType.APPLICATION_JSON)
public class HelloWorldResource {
    private final String template;
    private final String defaultName;
    private final AtomicLong counter;

    public HelloWorldResource(String template, String defaultName) {
        this.template = template;
        this.defaultName = defaultName;
        this.counter = new AtomicLong();
    }

    @GET
    public Saying sayHello(@QueryParam("name") Optional<String> name) {
        final String value = String.format(template, name.orElse(defaultName));
        return new Saying(counter.incrementAndGet(), value);
    }
}
```
And the `Saying` representation:
```java
// src/main/java/com/example/my_app/api/Saying.java
package com.example.my_app.api;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.Length;

public class Saying {
    private long id;

    @Length(max = 3)
    private String content;

    public Saying() {
        // Jackson deserialization
    }

    public Saying(long id, String content) {
        this.id = id;
        this.content = content;
    }

    @JsonProperty
    public long getId() {
        return id;
    }

    @JsonProperty
    public String getContent() {
        return content;
    }
}
```

**Q: How do I write tests for my DropWizard application?**
A: Use the `dropwizard-testing` module.
For resource testing:
```java
// src/test/java/com/example/my_app/resources/HelloWorldResourceTest.java
package com.example.my_app.resources;

import com.example.my_app.api.Saying;
import io.dropwizard.testing.junit5.DropwizardExtensionsSupport;
import io.dropwizard.testing.junit5.ResourceExtension;
import jakarta.ws.rs.core.Response;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(DropwizardExtensionsSupport.class)
public class HelloWorldResourceTest {
    private static final ResourceExtension EXT = ResourceExtension.builder()
        .forResource(new HelloWorldResource("Hello, %s!", "Stranger"))
        .build();

    @Test
    void sayHello() {
        final Saying saying = EXT.target("/hello-world")
            .queryParam("name", "Tester")
            .request()
            .get(Saying.class);
        assertThat(saying.getId()).isEqualTo(1);
        assertThat(saying.getContent()).isEqualTo("Hello, Tester!");
    }

    @Test
    void sayHelloWithoutName() {
        final Saying saying = EXT.target("/hello-world")
            .request()
            .get(Saying.class);
        assertThat(saying.getId()).isEqualTo(1);
        assertThat(saying.getContent()).isEqualTo("Hello, Stranger!");
    }
}
```
For application integration testing:
```java
// src/test/java/com/example/my_app/MyAppIntegrationTest.java
package com.example.my_app;

import io.dropwizard.testing.ResourceHelpers;
import io.dropwizard.testing.junit5.DropwizardAppExtension;
import io.dropwizard.testing.junit5.DropwizardExtensionsSupport;
import jakarta.ws.rs.client.Client;
import jakarta.ws.rs.core.Response;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(DropwizardExtensionsSupport.class)
public class MyAppIntegrationTest {
    private static final String CONFIG_PATH = ResourceHelpers.resourceFilePath("config.yml");

    public static final DropwizardAppExtension<MyAppConfiguration> APP = new DropwizardAppExtension<>(
        MyAppApplication.class, CONFIG_PATH
    );

    @Test
    void runHealthCheck() {
        Client client = APP.client();
        Response response = client.target(
            String.format("http://localhost:%d/healthcheck", APP.getAdminPort()))
            .request()
            .get();
        assertThat(response.getStatus()).isEqualTo(200);
    }

    @Test
    void runHelloWorld() {
        Client client = APP.client();
        String response = client.target(
            String.format("http://localhost:%d/hello-world", APP.getLocalPort()))
            .queryParam("name", "IntegrationTest")
            .request()
            .get(String.class);
        assertThat(response).contains("Hello, IntegrationTest!");
    }
}
```

## 5. Anti-Patterns to Flag

### 5.1. Configuration Anti-Pattern
**BAD:** Hardcoding database credentials or API keys directly in `Application` or `Configuration` classes.
```java
// BAD: Hardcoded credentials
public class MyAppConfiguration extends Configuration {
    public String getDatabaseUrl() {
        return "jdbc:postgresql://localhost:5432/mydb";
    }
    public String getDatabaseUser() {
        return "admin";
    }
    // ...
}
```
**GOOD:** Using `config.yml` and environment variables for sensitive data.
```yaml
# config.yml
database:
  url: ${DATABASE_URL:-jdbc:postgresql://localhost:5432/mydb}
  user: ${DATABASE_USER:-admin}
  password: ${DATABASE_PASSWORD} # Expects environment variable
```
```java
// GOOD: Configuration class reading from YAML
public class MyAppConfiguration extends Configuration {
    @JsonProperty("database")
    private DataSourceFactory database = new DataSourceFactory();

    public DataSourceFactory getDataSourceFactory() {
        return database;
    }

    @JsonProperty("database")
    public void setDataSourceFactory(DataSourceFactory database) {
        this.database = database;
    }
}
```

### 5.2. Resource Logic Anti-Pattern
**BAD:** Placing complex business logic directly within JAX-RS resource methods.
```java
// BAD: Resource doing too much
@Path("/orders")
public class OrderResource {
    @POST
    public Response createOrder(Order order) {
        // Complex validation, database operations, external service calls directly here
        if (order.getTotal() < 0) {
            return Response.status(400).entity("Invalid total").build();
        }
        // ... many lines of business logic ...
        return Response.ok(createdOrder).build();
    }
}
```
**GOOD:** Delegating business logic to separate service or manager classes.
```java
// GOOD: Resource delegates to a service
@Path("/orders")
public class OrderResource {
    private final OrderService orderService;

    public OrderResource(OrderService orderService) {
        this.orderService = orderService;
    }

    @POST
    public Response createOrder(Order order) {
        try {
            Order createdOrder = orderService.createOrder(order);
            return Response.status(201).entity(createdOrder).build();
        } catch (ValidationException e) {
            return Response.status(400).entity(e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(500).entity("Internal server error").build();
        }
    }
}

// OrderService.java
public class OrderService {
    private final OrderDAO orderDAO;
    private final PaymentGateway paymentGateway;

    public OrderService(OrderDAO orderDAO, PaymentGateway paymentGateway) {
        this.orderDAO = orderDAO;
        this.paymentGateway = paymentGateway;
    }

    public Order createOrder(Order order) throws ValidationException {
        // Perform validation
        if (order.getTotal() < 0) {
            throw new ValidationException("Invalid total");
        }
        // Process payment
        paymentGateway.processPayment(order.getPaymentInfo());
        // Save to database
        return orderDAO.save(order);
    }
}
```

## 6. Code Review Checklist

- [ ] Is configuration externalized and sensitive data handled securely (e.g., environment variables)?
- [ ] Are all critical dependencies covered by health checks?
- [ ] Is the application properly instrumented with DropWizard Metrics?
- [ ] Is logging configured for structured output and appropriate levels?
- [ ] Are all API inputs and outputs validated using Hibernate Validator?
- [ ] Is business logic separated from resource classes into dedicated service layers?
- [ ] Are unit and integration tests present, utilizing `dropwizard-testing`?
- [ ] Is the application packaged as a fat JAR?
- [ ] Is there a `Dockerfile` for containerization?
- [ ] Are there clear `README.md` and `SKILL.md` files for the project?

## 7. Related Skills

- `java-development-best-practices`: For general Java coding standards and patterns.
- `maven-build-automation`: For advanced Maven build configurations.
- `docker-containerization`: For best practices in Dockerizing applications.
- `kubernetes-orchestration`: For deploying and managing DropWizard services on Kubernetes.
- `ci-cd-pipelines`: For integrating DropWizard builds and deployments into CI/CD workflows.
- `rest-api-design`: For general principles of designing robust RESTful APIs.

## 8. Examples Directory Structure

```
examples/
├── basic-app/
│   ├── pom.xml
│   ├── src/
│   │   ├── main/java/com/example/basic/
│   │   │   ├── BasicApplication.java
│   │   │   ├── BasicConfiguration.java
│   │   │   ├── api/
│   │   │   │   └── Message.java
│   │   │   └── resources/
│   │   │       └── BasicResource.java
│   │   └── main/resources/
│   │       └── config.yml
│   │   └── test/java/com/example/basic/
│   │       ├── resources/
│   │       │   └── BasicResourceTest.java
│   │       └── BasicApplicationTest.java
│   └── README.md
├── advanced-features/
│   ├── database-integration/
│   │   ├── pom.xml
│   │   ├── src/
│   │   │   ├── main/java/com/example/db/
│   │   │   │   ├── DbApplication.java
│   │   │   │   ├── DbConfiguration.java
│   │   │   │   ├── core/
│   │   │   │   │   └── User.java
│   │   │   │   ├── db/
│   │   │   │   │   └── UserDAO.java
│   │   │   │   └── resources/
│   │   │   │       └── UserResource.java
│   │   │   └── main/resources/
│   │   │       └── config.yml
│   │   └── test/java/com/example/db/
│   │       ├── db/
│   │       │   └── UserDAOTest.java
│   │       └── resources/
│   │           └── UserResourceTest.java
│   └── metrics-healthchecks/
│       └── ... (similar structure)
└── README.md
```

## 9. Custom Scripts Section

Here are 3-5 automation scripts that would save significant time for DropWizard developers:

1.  **`create-dropwizard-project.sh`**: A shell script to quickly scaffold a new DropWizard project using the Maven archetype, handling common setup steps.
2.  **`generate-resource.sh`**: A shell script to generate boilerplate for a new JAX-RS resource, including its corresponding representation and basic test files.
3.  **`run-tests-with-containers.sh`**: A shell script to run DropWizard integration tests using `Testcontainers`, ensuring external dependencies are properly managed.
4.  **`build-and-dockerize.sh`**: A shell script to build the DropWizard fat JAR and then create a Docker image for the application.
5.  **`deploy-to-kubernetes.py`**: A Python script to generate basic Kubernetes deployment and service YAMLs for a DropWizard application, and optionally apply them.

```