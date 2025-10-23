package handler

import (
	"net/http"
	"context"

	"github.com/gin-gonic/gin"
	"github.com/your-username/gin-api/internal/service"
	"github.com/your-username/gin-api/internal/model"
	"errors"
)

type UserHandler struct {
	userService service.UserService
}

func NewUserHandler(userService service.UserService) *UserHandler {
	return &UserHandler{
		userService: userService,
	}
}

// @Summary Get all users
// @Description Get a list of all users
// @Tags User
// @Accept json
// @Produce json
// @Success 200 {array} model.User
// @Failure 500 {object} map[string]string
// @Router /users [get]
func (h *UserHandler) GetUsers(c *gin.Context) {
	ctx := c.Request.Context()
	users, err := h.userService.GetAllUsers(ctx)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, users)
}

// @Summary Get a user by ID
// @Description Get a single user by its ID
// @Tags User
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 200 {object} model.User
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users/{id} [get]
func (h *UserHandler) GetUserByID(c *gin.Context) {
	id := c.Param("id")
	ctx := c.Request.Context()
	user, err := h.userService.GetUserByID(ctx, id)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) { // Assuming ErrNotFound is a custom error from service
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, user)
}

// @Summary Create a new user
// @Description Create a new user with the provided data
// @Tags User
// @Accept json
// @Produce json
// @Param user body model.User true "Resource object to create"
// @Success 201 {object} model.User
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users [post]
func (h *UserHandler) CreateUser(c *gin.Context) {
	var user model.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	ctx := c.Request.Context()
	createdUser, err := h.userService.CreateUser(ctx, &user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, createdUser)
}

// @Summary Update an existing user
// @Description Update a user by ID with the provided data
// @Tags User
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Param user body model.User true "Resource object to update"
// @Success 200 {object} model.User
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users/{id} [put]
func (h *UserHandler) UpdateUser(c *gin.Context) {
	id := c.Param("id")
	var user model.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	user.ID = id // Ensure ID from path is used

	ctx := c.Request.Context()
	updatedUser, err := h.userService.UpdateUser(ctx, &user)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, updatedUser)
}

// @Summary Delete a user
// @Description Delete a user by its ID
// @Tags User
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 204 "No Content"
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /users/{id} [delete]
func (h *UserHandler) DeleteUser(c *gin.Context) {
	id := c.Param("id")
	ctx := c.Request.Context()
	err := h.userService.DeleteUser(ctx, id)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.Status(http.StatusNoContent)
}
