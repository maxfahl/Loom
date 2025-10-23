package config

import (
	"log"
	"os"
	"strconv"
)

type AppConfig struct {
	Port        string
	DatabaseURL string
	Environment string
	// Add other configuration fields as needed
}

func LoadConfig() *AppConfig {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port
	}

	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		log.Println("WARNING: DATABASE_URL not set, using default (in-memory store).")
		// In a real app, you might want to fatal here or use a default in-memory DB
		databaseURL = "in-memory"
	}

	environment := os.Getenv("ENVIRONMENT")
	if environment == "" {
		environment = "development"
	}

	return &AppConfig{
		Port:        port,
		DatabaseURL: databaseURL,
		Environment: environment,
	}
}

// GetBoolEnv reads a boolean environment variable with a default value.
func GetBoolEnv(key string, defaultValue bool) bool {
	val := os.Getenv(key)
	if val == "" {
		return defaultValue
	}
	b, err := strconv.ParseBool(val)
	if err != nil {
		log.Printf("WARNING: Invalid boolean value for %s: %s, using default %v", key, val, defaultValue)
		return defaultValue
	}
	return b
}

// GetIntEnv reads an integer environment variable with a default value.
func GetIntEnv(key string, defaultValue int) int {
	val := os.Getenv(key)
	if val == "" {
		return defaultValue
	}
	i, err := strconv.Atoi(val)
	if err != nil {
		log.Printf("WARNING: Invalid integer value for %s: %s, using default %d", key, val, defaultValue)
		return defaultValue
	}
	return i
}
