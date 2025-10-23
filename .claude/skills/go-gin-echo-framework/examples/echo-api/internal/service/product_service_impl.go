package service

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/your-username/echo-api/internal/model"
	"github.com/your-username/echo-api/internal/repository"
)

type productService struct {
	productRepo repository.ProductRepository
}

func NewProductService(productRepo repository.ProductRepository) ProductService {
	return &productService{
		productRepo: productRepo,
	}
}

func (s *productService) GetAllProducts(ctx context.Context) ([]model.Product, error) {
	products, err := s.productRepo.GetAll(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get all products: %w", err)
	}
	return products, nil
}

func (s *productService) GetProductByID(ctx context.Context, id string) (*model.Product, error) {
	product, err := s.productRepo.GetByID(ctx, id)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return nil, ErrNotFound // Translate repository error to service-level error
		}
		return nil, fmt.Errorf("failed to get product by ID: %w", err)
	}
	return product, nil
}

func (s *productService) CreateProduct(ctx context.Context, product *model.Product) (*model.Product, error) {
	// Add business logic here, e.g., validation, default values
	if product.ID == "" {
		product.ID = fmt.Sprintf("product-%d", time.Now().UnixNano()) // Example: generate ID
	}

	createdProduct, err := s.productRepo.Create(ctx, product)
	if err != nil {
		return nil, fmt.Errorf("failed to create product: %w", err)
	}
	return createdProduct, nil
}

func (s *productService) UpdateProduct(ctx context.Context, product *model.Product) (*model.Product, error) {
	// Add business logic here
	updatedProduct, err := s.productRepo.Update(ctx, product)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return nil, ErrNotFound
		}
		return nil, fmt.Errorf("failed to update product: %w", err)
	}
	return updatedProduct, nil
}

func (s *productService) DeleteProduct(ctx context.Context, id string) error {
	err := s.productRepo.Delete(ctx, id)
	if err != nil {
		if errors.Is(err, repository.ErrNotFound) {
			return ErrNotFound
		}
		return fmt.Errorf("failed to delete product: %w", err)
	}
	return nil
}
