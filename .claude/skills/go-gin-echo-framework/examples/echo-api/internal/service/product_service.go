package service

import (
	"context"
	"errors"
	"github.com/your-username/echo-api/internal/model"
)

var ErrNotFound = errors.New("not found")

type ProductService interface {
	GetAllProducts(ctx context.Context) ([]model.Product, error)
	GetProductByID(ctx context.Context, id string) (*model.Product, error)
	CreateProduct(ctx context.Context, product *model.Product) (*model.Product, error)
	UpdateProduct(ctx context.Context, product *model.Product) (*model.Product, error)
	DeleteProduct(ctx context.Context, id string) error
}
