package service

import (
	"context"
	"errors"
	"github.com/your-username/gin-api/internal/model"
)

var ErrNotFound = errors.New("not found")

type UserService interface {
	GetAllUsers(ctx context.Context) ([]model.User, error)
	GetUserByID(ctx context.Context, id string) (*model.User, error)
	CreateUser(ctx context.Context, user *model.User) (*model.User, error)
	UpdateUser(ctx context.Context, user *model.User) (*model.User, error)
	DeleteUser(ctx context.Context, id string) error
}
