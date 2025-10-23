package service

import (
	"context"
	"errors"
	"fmt"

	"github.com/your-username/gin-api/internal/model"
	"github.com/your-username/gin-api/internal/repository"
)

type userService struct {
	userRepo repository.UserRepository
}

func NewUserService(userRepo repository.UserRepository) UserService {
	return &userService{
		userRepo: userRepo,
	}
}

func (s *userService) GetAllUsers(ctx context.Context) ([]model.User, error) {
	users, err := s.userRepo.GetAll(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get all users: %w", err)
	}
	return users, nil
}

func (s *userService) GetUserByID(ctx context.Context, id string) (*model.User, error) {
	user, err := s.userRepo.GetByID(ctx, id)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return nil, ErrNotFound // Translate repository error to service-level error
		}
		return nil, fmt.Errorf("failed to get user by ID: %w", err)
	}
	return user, nil
}

func (s *userService) CreateUser(ctx context.Context, user *model.User) (*model.User, error) {
	// Add business logic here, e.g., validation, default values
	if user.ID == "" {
		user.ID = fmt.Sprintf("user-%d", time.Now().UnixNano()) // Example: generate ID
	}

	createdUser, err := s.userRepo.Create(ctx, user)
	if err != nil {
		return nil, fmt.Errorf("failed to create user: %w", err)
	}
	return createdUser, nil
}

func (s *userService) UpdateUser(ctx context.Context, user *model.User) (*model.User, error) {
	// Add business logic here
	updatedUser, err := s.userRepo.Update(ctx, user)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return nil, ErrNotFound
		}
		return nil, fmt.Errorf("failed to update user: %w", err)
	}
	return updatedUser, nil
}

func (s *userService) DeleteUser(ctx context.Context, id string) error {
	err := s.userRepo.Delete(ctx, id)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return ErrNotFound
		}
		return fmt.Errorf("failed to delete user: %w", err)
	}
	return nil
}
