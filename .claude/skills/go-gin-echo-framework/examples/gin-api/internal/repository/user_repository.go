package repository

import (
	"context"
	"errors"
	"github.com/your-username/gin-api/internal/model"
)

var ErrNotFound = errors.New("record not found")

type UserRepository interface {
	GetAll(ctx context.Context) ([]model.User, error)
	GetByID(ctx context.Context, id string) (*model.User, error)
	Create(ctx context.Context, user *model.User) (*model.User, error)
	Update(ctx context.Context, user *model.User) (*model.User, error)
	Delete(ctx context.Context, id string) error
}
