# Orders Service – Spring Boot + Docker

This document explains the architecture of the Orders Service, details the provided Dockerfile, and lists all common Maven commands with their flags.

## Architecture Overview

- **Framework:** Spring Boot 4 (Java 21)
- **Database:** MySQL (configured via Docker Compose)
- **Build Tool:** Maven
- **REST API:** Exposes endpoints (e.g., `/health`) using Spring WebMVC
- **Persistence:** Uses Spring Data JPA for ORM

### Key Files

- [`OrdersApplication.java`](src/main/java/dev/aryadanech/Orders/OrdersApplication.java): Main entry point.
- [`HealthController.java`](src/main/java/dev/aryadanech/Orders/controller/HealthController.java): Health check endpoint.
- [`application.properties`](src/main/resources/application.properties): Spring Boot configuration.
- [`pom.xml`](pom.xml): Maven project configuration.
- [`Dockerfile`](Dockerfile): Multi-stage Docker build.

## Dockerfile Explained

The Dockerfile uses a multi-stage build for efficient, production-ready images.

```dockerfile
# STEP 1 — Build the jar
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

COPY pom.xml .
RUN mvn -q -e -B dependency:resolve

COPY src ./src
RUN mvn -q -e -B package -DskipTests

# STEP 2 — Run the app
FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Stages

1. **Build Stage (`build`):**
   - Uses Maven with Java 21 to build the application.
   - Resolves dependencies and compiles the code.
   - Produces a fat JAR in `/app/target/`.

2. **Production Stage:**
   - Uses a lightweight Java 21 runtime.
   - Copies the built JAR from the build stage.
   - Exposes port 8080.
   - Runs the app with `java -jar app.jar`.


## Spring Boot Project Structure

- **Controller Layer:** Handles HTTP requests (e.g., [`HealthController`](src/main/java/dev/aryadanech/Orders/controller/HealthController.java)).
- **Service Layer:** (Add your business logic here.)
- **Repository Layer:** Interfaces for database access using Spring Data JPA.
- **Entity Layer:** Java classes mapped to database tables.
- **Configuration:** Application properties and environment variables.


## Running with Docker Compose

The service is orchestrated via [`docker-compose.yml`](../../../docker-compose.yml):

```yaml
orders_service:
  build:
    context: ./services/orders_service
  container_name: orders_service
  ports:
    - "8081:8080"
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://orders-db:3306/ordersdb
    SPRING_DATASOURCE_USERNAME: root
    SPRING_DATASOURCE_PASSWORD: root
  depends_on:
    - orders-db
```

**To start all services:**

```sh
docker compose up --build
```


## Maven Commands Table

| Command                        | Description                                 | Common Flags & Their Meaning                                                                                   |
|--------------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `mvn clean`                    | Cleans the target directory                 | `-q` (quiet), `-X` (debug), `-e` (show errors), `-B` (batch mode)                                            |
| `mvn compile`                  | Compiles the source code                    | `-q`, `-X`, `-e`, `-B`                                                                                        |
| `mvn test`                     | Runs tests                                  | `-q`, `-X`, `-e`, `-B`, `-Dtest=TestClass` (run specific test)                                               |
| `mvn package`                  | Packages the compiled code into a JAR       | `-q`, `-X`, `-e`, `-B`, `-DskipTests` (skip tests)                                                           |
| `mvn install`                  | Installs the JAR to local Maven repo        | `-q`, `-X`, `-e`, `-B`, `-DskipTests`                                                                        |
| `mvn spring-boot:run`          | Runs the Spring Boot app                    | `-q`, `-X`, `-e`, `-B`, `-Dspring-boot.run.profiles=dev` (set profile)                                       |
| `mvn dependency:resolve`       | Resolves dependencies                       | `-q`, `-X`, `-e`, `-B`                                                                                        |
| `mvn help:effective-pom`       | Shows the effective POM                     | `-q`, `-X`, `-e`, `-B`                                                                                        |
| `mvn validate`                 | Validates the project                       | `-q`, `-X`, `-e`, `-B`                                                                                        |
| `mvn verify`                   | Runs integration tests                      | `-q`, `-X`, `-e`, `-B`                                                                                        |

**Flag meanings:**

- `-q` or `--quiet`: Minimal output
- `-X` or `--debug`: Debug output
- `-e` or `--errors`: Show stack traces on errors
- `-B` or `--batch-mode`: Non-interactive (for CI/CD and docker builds)
- `-DskipTests`: Skip running tests
- `-Dtest=TestClass`: Run a specific test class
- `-Dspring-boot.run.profiles=dev`: Set Spring profile


## Example Maven Workflows

**Build the Project:**
```sh
mvn clean package -B -DskipTests
```

**Run the Application:**
```sh
mvn spring-boot:run -B
```

**Run Tests:**
```sh
mvn test -B
```

**Clean Build Artifacts:**
```sh
mvn clean -B
```

**Build Docker Image:**
```sh
docker build -t orders-service .
```


## Spring Boot Endpoints

- **Health Check:**  
  `GET /health`  
  Returns DB connectivity status.

## Environment Configuration

- **Database URL:** Set via `SPRING_DATASOURCE_URL` (see `docker-compose.yml`).
- **Other properties:** See [`application.properties`](src/main/resources/application.properties).
