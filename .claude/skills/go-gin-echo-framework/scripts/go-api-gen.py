import argparse
import os
import re

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_handler_gin(resource_name, module_path):
    snake_resource = to_snake_case(resource_name)
    camel_resource = resource_name # Assuming resource_name is already CamelCase for struct names
    lower_resource = resource_name.lower()

    content = f"""package handler

import (
	"net/http"
	"context"

	"github.com/gin-gonic/gin"
	"{module_path}/internal/service"
	"{module_path}/internal/model"
)

type {camel_resource}Handler struct {{
	{lower_resource}Service service.{camel_resource}Service
}}

func New{camel_resource}Handler({lower_resource}Service service.{camel_resource}Service) *{camel_resource}Handler {{
	return &{camel_resource}Handler{{
		{lower_resource}Service: {lower_resource}Service,
	}}
}}

// @Summary Get all {snake_resource}s
// @Description Get a list of all {snake_resource}s
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Success 200 {{array}} model.{camel_resource}
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s [get]
func (h *{camel_resource}Handler) Get{camel_resource}s(c *gin.Context) {{
	ctx := c.Request.Context()
	{lower_resource}s, err := h.{lower_resource}Service.GetAll{camel_resource}s(ctx)
	if err != nil {{
		c.JSON(http.StatusInternalServerError, gin.H{{"error": err.Error()}})
		return
	}}
	c.JSON(http.StatusOK, {lower_resource}s)
}}

// @Summary Get a {snake_resource} by ID
// @Description Get a single {snake_resource} by its ID
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 200 {{object}} model.{camel_resource}
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [get]
func (h *{camel_resource}Handler) Get{camel_resource}ByID(c *gin.Context) {{
	id := c.Param("id")
	ctx := c.Request.Context()
	{lower_resource}, err := h.{lower_resource}Service.Get{camel_resource}ByID(ctx, id)
	if err != nil {{
		if err.Error() == "not found" {{ // Example error handling
			c.JSON(http.StatusNotFound, gin.H{{"error": "{resource_name} not found"}})
			return
		}}
		c.JSON(http.StatusInternalServerError, gin.H{{"error": err.Error()}})
		return
	}}
	c.JSON(http.StatusOK, {lower_resource})
}}

// @Summary Create a new {snake_resource}
// @Description Create a new {snake_resource} with the provided data
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param {lower_resource} body model.{camel_resource} true "Resource object to create"
// @Success 201 {{object}} model.{camel_resource}
// @Failure 400 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s [post]
func (h *{camel_resource}Handler) Create{camel_resource}(c *gin.Context) {{
	var {lower_resource} model.{camel_resource}
	if err := c.ShouldBindJSON(&{lower_resource}); err != nil {{
		c.JSON(http.StatusBadRequest, gin.H{{"error": err.Error()}})
		return
	}}

	ctx := c.Request.Context()
	created{camel_resource}, err := h.{lower_resource}Service.Create{camel_resource}(ctx, &{lower_resource})
	if err != nil {{
		c.JSON(http.StatusInternalServerError, gin.H{{"error": err.Error()}})
		return
	}}
	c.JSON(http.StatusCreated, created{camel_resource})
}}

// @Summary Update an existing {snake_resource}
// @Description Update a {snake_resource} by ID with the provided data
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Param {lower_resource} body model.{camel_resource} true "Resource object to update"
// @Success 200 {{object}} model.{camel_resource}
// @Failure 400 {{object}} map[string]string
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [put]
func (h *{camel_resource}Handler) Update{camel_resource}(c *gin.Context) {{
	id := c.Param("id")
	var {lower_resource} model.{camel_resource}
	if err := c.ShouldBindJSON(&{lower_resource}); err != nil {{
		c.JSON(http.StatusBadRequest, gin.H{{"error": err.Error()}})
		return
	}}
	{lower_resource}.ID = id // Ensure ID from path is used

	ctx := c.Request.Context()
	updated{camel_resource}, err := h.{lower_resource}Service.Update{camel_resource}(ctx, &{lower_resource})
	if err != nil {{
		if err.Error() == "not found" {{
			c.JSON(http.StatusNotFound, gin.H{{"error": "{resource_name} not found"}})
			return
		}}
		c.JSON(http.StatusInternalServerError, gin.H{{"error": err.Error()}})
		return
	}}
	c.JSON(http.StatusOK, updated{camel_resource})
}}

// @Summary Delete a {snake_resource}
// @Description Delete a {snake_resource} by its ID
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 204 "No Content"
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [delete]
func (h *{camel_resource}Handler) Delete{camel_resource}(c *gin.Context) {{
	id := c.Param("id")
	ctx := c.Request.Context()
	err := h.{lower_resource}Service.Delete{camel_resource}(ctx, id)
	if err != nil {{
		if err.Error() == "not found" {{
			c.JSON(http.StatusNotFound, gin.H{{"error": "{resource_name} not found"}})
			return
		}}
		c.JSON(http.StatusInternalServerError, gin.H{{"error": err.Error()}})
		return
	}}
	c.Status(http.StatusNoContent)
}}
"""
    return content

def generate_handler_echo(resource_name, module_path):
    snake_resource = to_snake_case(resource_name)
    camel_resource = resource_name
    lower_resource = resource_name.lower()

    content = f"""package handler

import (
	"net/http"
	"context"

	"github.com/labstack/echo/v4"
	"{module_path}/internal/service"
	"{module_path}/internal/model"
)

type {camel_resource}Handler struct {{
	{lower_resource}Service service.{camel_resource}Service
}}

func New{camel_resource}Handler({lower_resource}Service service.{camel_resource}Service) *{camel_resource}Handler {{
	return &{camel_resource}Handler{{
		{lower_resource}Service: {lower_resource}Service,
	}}
}}

// @Summary Get all {snake_resource}s
// @Description Get a list of all {snake_resource}s
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Success 200 {{array}} model.{camel_resource}
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s [get]
func (h *{camel_resource}Handler) Get{camel_resource}s(c echo.Context) error {{
	ctx := c.Request().Context()
	{lower_resource}s, err := h.{lower_resource}Service.GetAll{camel_resource}s(ctx)
	if err != nil {{
		return c.JSON(http.StatusInternalServerError, map[string]string{{"error": err.Error()}})
	}}
	return c.JSON(http.StatusOK, {lower_resource}s)
}}

// @Summary Get a {snake_resource} by ID
// @Description Get a single {snake_resource} by its ID
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 200 {{object}} model.{camel_resource}
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [get]
func (h *{camel_resource}Handler) Get{camel_resource}ByID(c echo.Context) error {{
	id := c.Param("id")
	ctx := c.Request().Context()
	{lower_resource}, err := h.{lower_resource}Service.Get{camel_resource}ByID(ctx, id)
	if err != nil {{
		if err.Error() == "not found" {{ // Example error handling
			return c.JSON(http.StatusNotFound, map[string]string{{"error": "{resource_name} not found"}})
		}}
		return c.JSON(http.StatusInternalServerError, map[string]string{{"error": err.Error()}})
	}}
	return c.JSON(http.StatusOK, {lower_resource})
}}

// @Summary Create a new {snake_resource}
// @Description Create a new {snake_resource} with the provided data
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param {lower_resource} body model.{camel_resource} true "Resource object to create"
// @Success 201 {{object}} model.{camel_resource}
// @Failure 400 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s [post]
func (h *{camel_resource}Handler) Create{camel_resource}(c echo.Context) error {{
	var {lower_resource} model.{camel_resource}
	if err := c.Bind(&{lower_resource}); err != nil {{
		return c.JSON(http.StatusBadRequest, map[string]string{{"error": err.Error()}})
	}}

	ctx := c.Request().Context()
	created{camel_resource}, err := h.{lower_resource}Service.Create{camel_resource}(ctx, &{lower_resource})
	if err != nil {{
		return c.JSON(http.StatusInternalServerError, map[string]string{{"error": err.Error()}})
	}}
	return c.JSON(http.StatusCreated, created{camel_resource})
}}

// @Summary Update an existing {snake_resource}
// @Description Update a {snake_resource} by ID with the provided data
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Param {lower_resource} body model.{camel_resource} true "Resource object to update"
// @Success 200 {{object}} model.{camel_resource}
// @Failure 400 {{object}} map[string]string
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [put]
func (h *{camel_resource}Handler) Update{camel_resource}(c echo.Context) error {{
	id := c.Param("id")
	var {lower_resource} model.{camel_resource}
	if err := c.Bind(&{lower_resource}); err != nil {{
		return c.JSON(http.StatusBadRequest, map[string]string{{"error": err.Error()}})
	}}
	{lower_resource}.ID = id // Ensure ID from path is used

	ctx := c.Request().Context()
	updated{camel_resource}, err := h.{lower_resource}Service.Update{camel_resource}(ctx, &{lower_resource})
	if err != nil {{
		if err.Error() == "not found" {{
			return c.JSON(http.StatusNotFound, map[string]string{{"error": "{resource_name} not found"}})
		}}
		return c.JSON(http.StatusInternalServerError, map[string]string{{"error": err.Error()}})
	}}
	return c.JSON(http.StatusOK, updated{camel_resource})
}}

// @Summary Delete a {snake_resource}
// @Description Delete a {snake_resource} by its ID
// @Tags {resource_name}
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 204 "No Content"
// @Failure 404 {{object}} map[string]string
// @Failure 500 {{object}} map[string]string
// @Router /{snake_resource}s/{{id}} [delete]
func (h *{camel_resource}Handler) Delete{camel_resource}(c echo.Context) error {{
	id := c.Param("id")
	ctx := c.Request().Context()
	err := h.{lower_resource}Service.Delete{camel_resource}(ctx, id)
	if err != nil {{
		if err.Error() == "not found" {{
			return c.JSON(http.StatusNotFound, map[string]string{{"error": "{resource_name} not found"}})
		}}
		return c.JSON(http.StatusInternalServerError, map[string]string{{"error": err.Error()}})
	}}
	return c.NoContent(http.StatusNoContent)
}}
"""
    return content

def generate_service_interface(resource_name, module_path):
    camel_resource = resource_name
    content = f"""package service

import (
	"context"
	"{module_path}/internal/model"
)

type {camel_resource}Service interface {{
	GetAll{camel_resource}s(ctx context.Context) ([]model.{camel_resource}, error)
	Get{camel_resource}ByID(ctx context.Context, id string) (*model.{camel_resource}, error)
	Create{camel_resource}(ctx context.Context, {to_camel_case(resource_name)} *model.{camel_resource}) (*model.{camel_resource}, error)
	Update{camel_resource}(ctx context.Context, {to_camel_case(resource_name)} *model.{camel_resource}) (*model.{camel_resource}, error)
	Delete{camel_resource}(ctx context.Context, id string) error
}}
"""
    return content

def generate_service_implementation(resource_name, module_path):
    camel_resource = resource_name
    lower_resource = resource_name.lower()
    content = f"""package service

import (
	"context"
	"errors"
	"fmt"

	"{module_path}/internal/model"
	"{module_path}/internal/repository"
)

type {lower_resource}Service struct {{
	{lower_resource}Repo repository.{camel_resource}Repository
}}

func New{camel_resource}Service({lower_resource}Repo repository.{camel_resource}Repository) *{lower_resource}Service {{
	return &{lower_resource}Service{{
		{lower_resource}Repo: {lower_resource}Repo,
	}}
}}

func (s *{lower_resource}Service) GetAll{camel_resource}s(ctx context.Context) ([]model.{camel_resource}, error) {{
	{lower_resource}s, err := s.{lower_resource}Repo.GetAll(ctx)
	if err != nil {{
		return nil, fmt.Errorf("failed to get all {lower_resource}s: %w", err)
	}}
	return {lower_resource}s, nil
}}

func (s *{lower_resource}Service) Get{camel_resource}ByID(ctx context.Context, id string) (*model.{camel_resource}, error) {{
	{lower_resource}, err := s.{lower_resource}Repo.GetByID(ctx, id)
	if err != nil {{
		if errors.Is(err, repository.ErrNotFound) {{
			return nil, errors.New("not found") // Translate repository error to service-level error
		}}
		return nil, fmt.Errorf("failed to get {lower_resource} by ID: %w", err)
	}}
	return {lower_resource}, nil
}}

func (s *{lower_resource}Service) Create{camel_resource}(ctx context.Context, {lower_resource} *model.{camel_resource}) (*model.{camel_resource}, error) {{
	// Add business logic here, e.g., validation, default values
	if {lower_resource}.ID == "" {{
		{lower_resource}.ID = "generated-id" // Example: generate ID
	}}

	created{camel_resource}, err := s.{lower_resource}Repo.Create(ctx, {lower_resource})
	if err != nil {{
		return nil, fmt.Errorf("failed to create {lower_resource}: %w", err)
	}}
	return created{camel_resource}, nil
}}

func (s *{lower_resource}Service) Update{camel_resource}(ctx context.Context, {lower_resource} *model.{camel_resource}) (*model.{camel_resource}, error) {{
	// Add business logic here
	updated{camel_resource}, err := s.{lower_resource}Repo.Update(ctx, {lower_resource})
	if err != nil {{
		if errors.Is(err, repository.ErrNotFound) {{
			return nil, errors.New("not found")
		}}
		return nil, fmt.Errorf("failed to update {lower_resource}: %w", err)
	}}
	return updated{camel_resource}, nil
}}

func (s *{lower_resource}Service) Delete{camel_resource}(ctx context.Context, id string) error {{
	err := s.{lower_resource}Repo.Delete(ctx, id)
	if err != nil {{
		if errors.Is(err, repository.ErrNotFound) {{
			return errors.New("not found")
		}}
		return fmt.Errorf("failed to delete {lower_resource}: %w", err)
	}}
	return nil
}}
"""
    return content

def generate_repository_interface(resource_name, module_path):
    camel_resource = resource_name
    content = f"""package repository

import (
	"context"
	"errors"
	"{module_path}/internal/model"
)

var ErrNotFound = errors.New("record not found")

type {camel_resource}Repository interface {{
	GetAll(ctx context.Context) ([]model.{camel_resource}, error)
	GetByID(ctx context.Context, id string) (*model.{camel_resource}, error)
	Create(ctx context.Context, {to_camel_case(resource_name)} *model.{camel_resource}) (*model.{camel_resource}, error)
	Update(ctx context.Context, {to_camel_case(resource_name)} *model.{camel_resource}) (*model.{camel_resource}, error)
	Delete(ctx context.Context, id string) error
}}
"""
    return content

def generate_repository_implementation(resource_name, module_path):
    camel_resource = resource_name
    lower_resource = resource_name.lower()
    content = f"""package repository

import (
	"context"
	"fmt"

	"{module_path}/internal/model"
)

// In-memory store for demonstration purposes
var {lower_resource}sStore = make(map[string]model.{camel_resource})

type {lower_resource}Repository struct {{
	// db *sql.DB // In a real application, this would be a database connection
}}

func New{camel_resource}Repository(/* db *sql.DB */) *{lower_resource}Repository {{
	return &{lower_resource}Repository{{
		// db: db,
	}}
}}

func (r *{lower_resource}Repository) GetAll(ctx context.Context) ([]model.{camel_resource}, error) {{
	// Simulate database call
	var all{camel_resource}s []model.{camel_resource}
	for _, {lower_resource} := range {lower_resource}sStore {{
		all{camel_resource}s = append(all{camel_resource}s, {lower_resource})
	}}
	return all{camel_resource}s, nil
}}

func (r *{lower_resource}Repository) GetByID(ctx context.Context, id string) (*model.{camel_resource}, error) {{
	// Simulate database call
	{lower_resource}, ok := {lower_resource}sStore[id]
	if !ok {{
		return nil, ErrNotFound
	}}
	return &{lower_resource}, nil
}}

func (r *{lower_resource}Repository) Create(ctx context.Context, {lower_resource} *model.{camel_resource}) (*model.{camel_resource}, error) {{
	// Simulate database call
	if _, exists := {lower_resource}sStore[{lower_resource}.ID]; exists {{
		return nil, fmt.Errorf("{lower_resource} with ID %s already exists", {lower_resource}.ID)
	}}
	{lower_resource}sStore[{lower_resource}.ID] = *{lower_resource}
	return {lower_resource}, nil
}}

func (r *{lower_resource}Repository) Update(ctx context.Context, {lower_resource} *model.{camel_resource}) (*model.{camel_resource}, error) {{
	// Simulate database call
	if _, exists := {lower_resource}sStore[{lower_resource}.ID]; !exists {{
		return nil, ErrNotFound
	}}
	{lower_resource}sStore[{lower_resource}.ID] = *{lower_resource}
	return {lower_resource}, nil
}}

func (r *{lower_resource}Repository) Delete(ctx context.Context, id string) error {{
	// Simulate database call
	if _, exists := {lower_resource}sStore[id]; !exists {{
		return ErrNotFound
	}}
	delete({lower_resource}sStore, id)
	return nil
}}
"""
    return content

def generate_model(resource_name):
    camel_resource = resource_name
    content = f"""package model

type {camel_resource} struct {{
	ID   string `json:"id"`
	Name string `json:"name"`
	// Add more fields as needed
}}
"""
    return content

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate code for a new API resource in Go (Gin/Echo).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--framework", required=True, choices=["gin", "echo"],
                        help="The web framework to use (gin or echo).")
    parser.add_argument("--resource", required=True,
                        help="The name of the resource (e.g., User, Product). Should be in CamelCase.")
    parser.add_argument("--output-dir", default=".",
                        help="The base output directory for generated files (e.g., internal).")
    parser.add_argument("--module-path", required=True,
                        help="The Go module path of the project (e.g., github.com/myuser/myproject).")
    parser.add_argument("--crud", action="store_true",
                        help="Generate basic CRUD methods for the resource.")

    args = parser.parse_args()

    framework = args.framework
    resource_name = args.resource
    output_dir = args.output_dir
    module_path = args.module_path
    generate_crud = args.crud

    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', resource_name):
        print(f"Error: Resource name '{resource_name}' must be in CamelCase (e.g., User, Product).")
        exit(1)

    # Ensure output directories exist
    os.makedirs(os.path.join(output_dir, "model"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "handler"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "service"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "repository"), exist_ok=True)

    print(f"Generating {resource_name} resource for {framework} framework in {output_dir}...")

    # Generate Model
    model_content = generate_model(resource_name)
    model_file_path = os.path.join(output_dir, "model", f"{to_snake_case(resource_name)}.go")
    with open(model_file_path, "w") as f:
        f.write(model_content)
    print(f"Created: {model_file_path}")

    # Generate Handler
    if framework == "gin":
        handler_content = generate_handler_gin(resource_name, module_path)
    else: # echo
        handler_content = generate_handler_echo(resource_name, module_path)
    handler_file_path = os.path.join(output_dir, "handler", f"{to_snake_case(resource_name)}_handler.go")
    with open(handler_file_path, "w") as f:
        f.write(handler_content)
    print(f"Created: {handler_file_path}")

    # Generate Service Interface
    service_interface_content = generate_service_interface(resource_name, module_path)
    service_interface_file_path = os.path.join(output_dir, "service", f"{to_snake_case(resource_name)}_service.go")
    with open(service_interface_file_path, "w") as f:
        f.write(service_interface_content)
    print(f"Created: {service_interface_file_path}")

    # Generate Service Implementation
    service_impl_content = generate_service_implementation(resource_name, module_path)
    service_impl_file_path = os.path.join(output_dir, "service", f"{to_snake_case(resource_name)}_service_impl.go")
    with open(service_impl_file_path, "w") as f:
        f.write(service_impl_content)
    print(f"Created: {service_impl_file_path}")

    # Generate Repository Interface
    repo_interface_content = generate_repository_interface(resource_name, module_path)
    repo_interface_file_path = os.path.join(output_dir, "repository", f"{to_snake_case(resource_name)}_repository.go")
    with open(repo_interface_file_path, "w") as f:
        f.write(repo_interface_content)
    print(f"Created: {repo_interface_file_path}")

    # Generate Repository Implementation
    repo_impl_content = generate_repository_implementation(resource_name, module_path)
    repo_impl_file_path = os.path.join(output_dir, "repository", f"{to_snake_case(resource_name)}_repository_impl.go")
    with open(repo_impl_file_path, "w") as f:
        f.write(repo_impl_content)
    print(f"Created: {repo_impl_file_path}")

    print(f"Successfully generated boilerplate for {resource_name} resource.")

if __name__ == "__main__":
    main()