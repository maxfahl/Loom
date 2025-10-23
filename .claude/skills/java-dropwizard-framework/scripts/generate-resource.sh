#!/bin/bash

# generate-resource.sh
#
# Purpose:
#   Generates boilerplate code for a new DropWizard JAX-RS resource, its corresponding
#   data representation (POJO), and basic test stubs. This automates the repetitive
#   task of setting up new API endpoints.
#
# Usage:
#   ./generate-resource.sh --name User --package com.example.my_app
#   ./generate-resource.sh --help
#
# Options:
#   --name          Name of the resource (e.g., User, Product). Will be capitalized.
#   --package       Base package of the application (e.g., com.example.my_app)
#   --dry-run       Show the files that would be created without actually creating them
#   --help          Display this help message

# --- Configuration ---
DRY_RUN=false

# --- Functions ---

# Function to display help message
display_help() {
    grep '^# Usage:' "$0" | sed -e 's/^# //' -e 's/^Usage:/Usage:\n /'
    grep '^# Options:' "$0" | sed -e 's/^# //' -e 's/^Options:/Options:\n/'
    exit 0
}

# Function to convert kebab-case or snake_case to PascalCase
to_pascal_case() {
    echo "$1" | sed -r 's/([-_][a-z])|([a-z])/(echo ${BASH_REMATCH[2]} | tr '[:lower:]' '[:upper:]')\1/g' | sed -r 's/[-_]//g'
}

# Function to convert PascalCase to kebab-case
to_kebab_case() {
    echo "$1" | sed -r 's/([A-Z])/-\L\1/g' | sed -e 's/^-//'
}

# --- Main Script Logic ---

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --name) RESOURCE_NAME_RAW="$2"; shift ;; 
        --package) BASE_PACKAGE="$2"; shift ;; 
        --dry-run) DRY_RUN=true ;; 
        --help) display_help ;; 
        *) echo "Unknown parameter passed: $1"; display_help ;; 
    esac
    shift
done

if [ -z "$RESOURCE_NAME_RAW" ] || [ -z "$BASE_PACKAGE" ]; then
    echo "Error: --name and --package are required."
    display_help
fi

RESOURCE_NAME=$(to_pascal_case "$RESOURCE_NAME_RAW")
RESOURCE_NAME_LOWER=$(to_kebab_case "$RESOURCE_NAME")

# Derive paths
MAIN_JAVA_DIR="src/main/java/$(echo "$BASE_PACKAGE" | tr '.' '/')"
TEST_JAVA_DIR="src/test/java/$(echo "$BASE_PACKAGE" | tr '.' '/')"

RESOURCE_DIR="${MAIN_JAVA_DIR}/resources"
API_DIR="${MAIN_JAVA_DIR}/api"
TEST_RESOURCE_DIR="${TEST_JAVA_DIR}/resources"
TEST_API_DIR="${TEST_JAVA_DIR}/api"

RESOURCE_FILE="${RESOURCE_DIR}/${RESOURCE_NAME}Resource.java"
API_FILE="${API_DIR}/${RESOURCE_NAME}.java"
TEST_RESOURCE_FILE="${TEST_RESOURCE_DIR}/${RESOURCE_NAME}ResourceTest.java"
TEST_API_FILE="${TEST_API_DIR}/${RESOURCE_NAME}Test.java"

PACKAGE_RESOURCES="${BASE_PACKAGE}.resources"
PACKAGE_API="${BASE_PACKAGE}.api"

echo "--- DropWizard Resource Generator ---"
echo "  Resource Name: $RESOURCE_NAME"
echo "  Base Package: $BASE_PACKAGE"
echo "  Resource Path: /${RESOURCE_NAME_LOWER}s"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "Dry run: The following files would be created:"
    echo "- $RESOURCE_FILE"
    echo "- $API_FILE"
    echo "- $TEST_RESOURCE_FILE"
    echo "- $TEST_API_FILE"
    exit 0
fi

# Create directories
mkdir -p "$RESOURCE_DIR"
mkdir -p "$API_DIR"
mkdir -p "$TEST_RESOURCE_DIR"
mkdir -p "$TEST_API_DIR"

# --- Generate Resource.java ---
cat <<EOF > "$RESOURCE_FILE"
package ${PACKAGE_RESOURCES};

import ${PACKAGE_API}.${RESOURCE_NAME};
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

@Path("/${RESOURCE_NAME_LOWER}s")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ${RESOURCE_NAME}Resource {

    private final AtomicLong counter = new AtomicLong();
    private final List<${RESOURCE_NAME}> ${RESOURCE_NAME_LOWER}s = new ArrayList<>();

    public ${RESOURCE_NAME}Resource() {
        // Initialize with some dummy data if needed
        ${RESOURCE_NAME_LOWER}s.add(new ${RESOURCE_NAME}(counter.incrementAndGet(), "Sample ${RESOURCE_NAME} 1"));
        ${RESOURCE_NAME_LOWER}s.add(new ${RESOURCE_NAME}(counter.incrementAndGet(), "Sample ${RESOURCE_NAME} 2"));
    }

    @GET
    public List<${RESOURCE_NAME}> getAll${RESOURCE_NAME}s() {
        return ${RESOURCE_NAME_LOWER}s;
    }

    @GET
    @Path("/{id}")
    public Response get${RESOURCE_NAME}(@PathParam("id") Long id) {
        Optional<${RESOURCE_NAME}> ${RESOURCE_NAME_LOWER} = ${RESOURCE_NAME_LOWER}s.stream()
            .filter(r -> r.getId() == id)
            .findFirst();
        return ${RESOURCE_NAME_LOWER}.map(r -> Response.ok(r).build())
            .orElse(Response.status(Response.Status.NOT_FOUND).build());
    }

    @POST
    public Response create${RESOURCE_NAME}(${RESOURCE_NAME} ${RESOURCE_NAME_LOWER}) {
        ${RESOURCE_NAME_LOWER}.setId(counter.incrementAndGet());
        ${RESOURCE_NAME_LOWER}s.add(${RESOURCE_NAME_LOWER});
        return Response.status(Response.Status.CREATED).entity(${RESOURCE_NAME_LOWER}).build();
    }

    @PUT
    @Path("/{id}")
    public Response update${RESOURCE_NAME}(@PathParam("id") Long id, ${RESOURCE_NAME} updated${RESOURCE_NAME}) {
        Optional<${RESOURCE_NAME}> existing${RESOURCE_NAME} = ${RESOURCE_NAME_LOWER}s.stream()
            .filter(r -> r.getId() == id)
            .findFirst();

        if (existing${RESOURCE_NAME}.isPresent()) {
            ${RESOURCE_NAME} resource = existing${RESOURCE_NAME}.get();
            resource.setContent(updated${RESOURCE_NAME}.getContent()); // Assuming a 'content' field
            return Response.ok(resource).build();
        } else {
            updated${RESOURCE_NAME}.setId(id);
            ${RESOURCE_NAME_LOWER}s.add(updated${RESOURCE_NAME});
            return Response.status(Response.Status.CREATED).entity(updated${RESOURCE_NAME}).build();
        }
    }

    @DELETE
    @Path("/{id}")
    public Response delete${RESOURCE_NAME}(@PathParam("id") Long id) {
        boolean removed = ${RESOURCE_NAME_LOWER}s.removeIf(r -> r.getId() == id);
        if (removed) {
            return Response.noContent().build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }
}
EOF

# --- Generate API.java (Representation) ---
cat <<EOF > "$API_FILE"
package ${PACKAGE_API};

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;

public class ${RESOURCE_NAME} {
    private long id;

    @NotBlank
    private String content;

    public ${RESOURCE_NAME}() {
        // Jackson deserialization
    }

    public ${RESOURCE_NAME}(long id, String content) {
        this.id = id;
        this.content = content;
    }

    @JsonProperty
    public long getId() {
        return id;
    }

    @JsonProperty
    public void setId(long id) {
        this.id = id;
    }

    @JsonProperty
    public String getContent() {
        return content;
    }

    @JsonProperty
    public void setContent(String content) {
        this.content = content;
    }
}
EOF

# --- Generate ResourceTest.java ---
cat <<EOF > "$TEST_RESOURCE_FILE"
package ${PACKAGE_RESOURCES};

import ${PACKAGE_API}.${RESOURCE_NAME};
import io.dropwizard.testing.junit5.DropwizardExtensionsSupport;
import io.dropwizard.testing.junit5.ResourceExtension;
import jakarta.ws.rs.client.Entity;
import jakarta.ws.rs.core.GenericType;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(DropwizardExtensionsSupport.class)
public class ${RESOURCE_NAME}ResourceTest {

    private static final ResourceExtension EXT = ResourceExtension.builder()
        .forResource(new ${RESOURCE_NAME}Resource())
        .build();

    @Test
    void testGetAll${RESOURCE_NAME}s() {
        List<${RESOURCE_NAME}> ${RESOURCE_NAME_LOWER}s = EXT.target("/${RESOURCE_NAME_LOWER}s")
            .request()
            .get(new GenericType<List<${RESOURCE_NAME}>>() {});
        assertThat(${RESOURCE_NAME_LOWER}s).hasSize(2);
        assertThat(${RESOURCE_NAME_LOWER}s.get(0).getContent()).isEqualTo("Sample ${RESOURCE_NAME} 1");
    }

    @Test
    void testGet${RESOURCE_NAME}ById() {
        ${RESOURCE_NAME} ${RESOURCE_NAME_LOWER} = EXT.target("/${RESOURCE_NAME_LOWER}s/1")
            .request()
            .get(${RESOURCE_NAME}.class);
        assertThat(${RESOURCE_NAME_LOWER}.getId()).isEqualTo(1L);
        assertThat(${RESOURCE_NAME_LOWER}.getContent()).isEqualTo("Sample ${RESOURCE_NAME} 1");
    }

    @Test
    void testGet${RESOURCE_NAME}NotFound() {
        Response response = EXT.target("/${RESOURCE_NAME_LOWER}s/99")
            .request()
            .get();
        assertThat(response.getStatus()).isEqualTo(Response.Status.NOT_FOUND.getStatusCode());
    }

    @Test
    void testCreate${RESOURCE_NAME}() {
        ${RESOURCE_NAME} new${RESOURCE_NAME} = new ${RESOURCE_NAME}(0L, "New ${RESOURCE_NAME}");
        Response response = EXT.target("/${RESOURCE_NAME_LOWER}s")
            .request()
            .post(Entity.entity(new${RESOURCE_NAME}, MediaType.APPLICATION_JSON));

        assertThat(response.getStatus()).isEqualTo(Response.Status.CREATED.getStatusCode());
        ${RESOURCE_NAME} created${RESOURCE_NAME} = response.readEntity(${RESOURCE_NAME}.class);
        assertThat(created${RESOURCE_NAME}.getId()).isGreaterThan(0L);
        assertThat(created${RESOURCE_NAME}.getContent()).isEqualTo("New ${RESOURCE_NAME}");
    }

    @Test
    void testUpdate${RESOURCE_NAME}() {
        ${RESOURCE_NAME} updated${RESOURCE_NAME} = new ${RESOURCE_NAME}(0L, "Updated ${RESOURCE_NAME} 1");
        Response response = EXT.target("/${RESOURCE_NAME_LOWER}s/1")
            .request()
            .put(Entity.entity(updated${RESOURCE_NAME}, MediaType.APPLICATION_JSON));

        assertThat(response.getStatus()).isEqualTo(Response.Status.OK.getStatusCode());
        ${RESOURCE_NAME} returned${RESOURCE_NAME} = response.readEntity(${RESOURCE_NAME}.class);
        assertThat(returned${RESOURCE_NAME}.getId()).isEqualTo(1L);
        assertThat(returned${RESOURCE_NAME}.getContent()).isEqualTo("Updated ${RESOURCE_NAME} 1");
    }

    @Test
    void testDelete${RESOURCE_NAME}() {
        Response response = EXT.target("/${RESOURCE_NAME_LOWER}s/1")
            .request()
            .delete();
        assertThat(response.getStatus()).isEqualTo(Response.Status.NO_CONTENT.getStatusCode());

        response = EXT.target("/${RESOURCE_NAME_LOWER}s/1")
            .request()
            .get();
        assertThat(response.getStatus()).isEqualTo(Response.Status.NOT_FOUND.getStatusCode());
    }
}
EOF

# --- Generate APITest.java (Representation Test) ---
cat <<EOF > "$TEST_API_FILE"
package ${PACKAGE_API};

import com.fasterxml.jackson.databind.ObjectMapper;
import io.dropwizard.jackson.Jackson;
import org.junit.jupiter.api.Test;

import static io.dropwizard.testing.FixtureHelpers.fixture;
import static org.assertj.core.api.Assertions.assertThat;

public class ${RESOURCE_NAME}Test {
    private static final ObjectMapper MAPPER = Jackson.newObjectMapper();

    @Test
    void serializesToJSON() throws Exception {
        final ${RESOURCE_NAME} ${RESOURCE_NAME_LOWER} = new ${RESOURCE_NAME}(1L, "Test Content");
        final String expected = MAPPER.writeValueAsString(MAPPER.readValue(fixture("fixtures/${RESOURCE_NAME_LOWER}.json"), ${RESOURCE_NAME}.class));
        assertThat(MAPPER.writeValueAsString(${RESOURCE_NAME_LOWER})).isEqualTo(expected);
    }

    @Test
    void deserializesFromJSON() throws Exception {
        final ${RESOURCE_NAME} ${RESOURCE_NAME_LOWER} = new ${RESOURCE_NAME}(1L, "Test Content");
        assertThat(MAPPER.readValue(fixture("fixtures/${RESOURCE_NAME_LOWER}.json"), ${RESOURCE_NAME}.class))
            .isEqualTo(${RESOURCE_NAME_LOWER});
    }
}
EOF

echo ""
echo "Successfully generated boilerplate for ${RESOURCE_NAME} resource."
echo "Files created:"
echo "- $RESOURCE_FILE"
echo "- $API_FILE"
echo "- $TEST_RESOURCE_FILE"
echo "- $TEST_API_FILE"
echo ""
echo "Remember to register your new resource in your DropWizard Application class (e.g., MyAppApplication.java):"
echo "  environment.jersey().register(new ${RESOURCE_NAME}Resource());"
echo "And create a fixture file for representation testing: src/test/resources/fixtures/${RESOURCE_NAME_LOWER}.json"
