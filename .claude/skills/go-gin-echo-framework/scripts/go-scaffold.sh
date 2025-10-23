#!/bin/bash

# go-scaffold.sh: Go Project Scaffolder
# Description: Automates the creation of a new Go web project with a best-practice directory structure,
#              go.mod initialization, basic server setup (Gin or Echo), and a Makefile for common tasks.
#
# Usage:
#   ./go-scaffold.sh <project_name> <framework> [--module <module_path>]
#
# Arguments:
#   project_name: The name of the new Go project.
#   framework:    The web framework to use (gin or echo).
#   --module:     Optional. The Go module path (e.g., github.com/user/project).
#                 If not provided, it defaults to <project_name>.
#
# Examples:
#   ./go-scaffold.sh my-gin-app gin
#   ./go-scaffold.sh another-echo-app echo --module github.com/myuser/another-app
#
# Features:
# - Creates a standard Go project layout (cmd, internal, config, handler, service, repository).
# - Initializes go.mod with the specified module path.
# - Sets up a basic HTTP server using either Gin or Echo.
# - Includes a basic Dockerfile for containerization.
# - Generates a Makefile for common development tasks (run, build, test, clean).
# - Installs the chosen web framework.
#
# Error Handling:
# - Exits if project_name or framework are not provided.
# - Exits if an invalid framework is specified.
# - Exits if directory creation or go mod init fails.
#
# Cross-platform: Designed for Unix-like systems (Linux, macOS, WSL).

set -e

# --- Configuration ---
DEFAULT_MODULE_PREFIX="github.com/your-username" # Customize if needed

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 <project_name> <framework> [--module <module_path>]"
    echo ""
    echo "Arguments:"
    echo "  project_name: The name of the new Go project."
    echo "  framework:    The web framework to use (gin or echo)."
    echo "  --module:     Optional. The Go module path (e.g., github.com/user/project)."
    echo "                If not provided, it defaults to $DEFAULT_MODULE_PREFIX/<project_name>."
    echo ""
    echo "Examples:"
    echo "  $0 my-gin-app gin"
    echo "  $0 another-echo-app echo --module github.com/myuser/another-app"
    exit 0
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
    exit 1
}

# --- Parse Arguments ---
PROJECT_NAME=""
FRAMEWORK=""
MODULE_PATH=""

while (( "$#" )); do
    case "$1" in
        --help)
            print_help
            ;; 
        --module)
            if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
                MODULE_PATH="$2"
                shift 2
            else
                log_error "Argument for --module is missing."
            fi
            ;; 
        -*)
            log_error "Unknown option: $1"
            ;; 
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            elif [ -z "$FRAMEWORK" ]; then
                FRAMEWORK="$1"
            else
                log_error "Too many arguments. See --help."
            fi
            shift
            ;; 
    esac
done

if [ -z "$PROJECT_NAME" ]; then
    log_error "Project name is required. See --help."
fi

if [ -z "$FRAMEWORK" ]; then
    log_error "Framework is required (gin or echo). See --help."
fi

if [ "$FRAMEWORK" != "gin" ] && [ "$FRAMEWORK" != "echo" ]; then
    log_error "Invalid framework specified: $FRAMEWORK. Must be 'gin' or 'echo'."
fi

if [ -z "$MODULE_PATH" ]; then
    MODULE_PATH="$DEFAULT_MODULE_PREFIX/$PROJECT_NAME"
fi

log_info "Scaffolding new Go project: $PROJECT_NAME"
log_info "Framework: $FRAMEWORK"
log_info "Module Path: $MODULE_PATH"

# --- Create Project Directory ---
mkdir -p "$PROJECT_NAME" || log_error "Failed to create project directory: $PROJECT_NAME"
cd "$PROJECT_NAME" || log_error "Failed to change to project directory: $PROJECT_NAME"

# --- Create Standard Go Project Layout ---
log_info "Creating standard Go project layout..."
mkdir -p cmd/api internal/config internal/handler internal/service internal/repository
touch internal/config/config.go internal/handler/handler.go internal/service/service.go internal/repository/repository.go

# --- Initialize Go Module ---
log_info "Initializing Go module: $MODULE_PATH"
go mod init "$MODULE_PATH" || log_error "Failed to initialize Go module."

# --- Add main.go ---
log_info "Creating cmd/api/main.go..."
MAIN_GO_CONTENT=""
if [ "$FRAMEWORK" == "gin" ]; then
    MAIN_GO_CONTENT='package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"context"
)

func main() {
	# Set Gin to production mode in production
	if os.Getenv("GIN_MODE") == "release" {
		gin.SetMode(gin.ReleaseMode)
	}

	router := gin.Default()

	# Middleware
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	# Simple health check endpoint
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "UP"})
	})

	# Example route
	router.GET("/hello", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Hello from Gin!"})
	})

	# Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	srv := &http.Server{
		Addr:    ":" + port,
		Handler: router,
	}

	# Graceful shutdown
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	# Wait for interrupt signal to gracefully shutdown the server with a timeout of 5 seconds.
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-
	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Server exiting")
}
'
elif [ "$FRAMEWORK" == "echo" ]; then
    MAIN_GO_CONTENT='package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()

	# Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	# Simple health check endpoint
	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "UP"})
	})

	# Example route
	e.GET("/hello", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "Hello from Echo!"})
	})

	# Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	# Graceful shutdown
	go func() {
		if err := e.Start(":