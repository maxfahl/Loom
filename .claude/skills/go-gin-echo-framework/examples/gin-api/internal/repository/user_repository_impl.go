package repository

import (
	"context"
	"fmt"

	"github.com/your-username/gin-api/internal/model"
)

// In-memory store for demonstration purposes
var usersStore = make(map[string]model.User)

type userRepository struct {
	// db *sql.DB // In a real application, this would be a database connection
}

func NewUserRepository(/* db *sql.DB */) UserRepository {
	return &userRepository{
		// db: db,
	}
}

func (r *userRepository) GetAll(ctx context.Context) ([]model.User, error) {
	// Simulate database call
	var allUsers []model.User
	for _, user := range usersStore {
		allUsers = append(allUsers, user)
	}
	return allUsers, nil
}

func (r *userRepository) GetByID(ctx context.Context, id string) (*model.User, error) {
	// Simulate database call
	user, ok := usersStore[id]
	if !ok {
		return nil, ErrNotFound
	}
	return &user, nil
}

func (r *userRepository) Create(ctx context.Context, user *model.User) (*model.User, error) {
	// Simulate database call
	if _, exists := usersStore[user.ID]; exists {
		return nil, fmt.Errorf("user with ID %s already exists", user.ID)
	}
	usersStore[user.ID] = *user
	return user, nil
}

func (r *userRepository) Update(ctx context.Context, user *model.User) (*model.User, error) {
	// Simulate database call
	if _, exists := usersStore[user.ID]; !exists {
		return nil, ErrNotFound
	}
	usersStore[user.ID] = *user
	return user, nil
}

func (r *userRepository) Delete(ctx context.Context, id string) error {
	// Simulate database call
	if _, exists := usersStore[id]; !exists {
		return ErrNotFound
	}
	delete(usersStore, id)
	return nil
}
