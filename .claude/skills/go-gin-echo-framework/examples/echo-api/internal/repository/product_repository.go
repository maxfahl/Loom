package repository

import (
	"context"
	"errors"
	"github.com/your-username/echo-api/internal/model"
)

var ErrNotFound = errors.New("record not found")

type ProductRepository interface {
	GetAll(ctx context.Context) ([]model.Product, error)
	GetByID(ctx context.Context, id string) (*model.Product, error)
	Create(ctx context.Context, product *model.Product) (*model.Product, error)
	Update(ctx context.Context, product *model.Product) (*model.Product, error)
	Delete(ctx context.Context, id string) error
}
