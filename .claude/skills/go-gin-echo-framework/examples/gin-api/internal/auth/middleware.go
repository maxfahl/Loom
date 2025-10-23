package auth

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// AuthMiddleware is a simple example of an authentication middleware.
func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// In a real application, you would validate a token (e.g., JWT) or session.
		// For demonstration, we'll just check for a specific header.
		token := c.GetHeader("Authorization")

		if token != "Bearer my-secret-token" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Unauthorized"})
			return
		}

		// If authenticated, you might set user information in the context
		// c.Set("userID", "123")

		c.Next()
	}
}
