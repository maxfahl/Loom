package repository

import (
	"context"
	"fmt"

	"github.com/your-username/echo-api/internal/model"
)

// In-memory store for demonstration purposes
var productsStore = make(map[string]model.Product)

type productRepository struct {
	// db *sql.DB // In a real application, this would be a database connection
}

func NewProductRepository(/* db *sql.DB */) ProductRepository {
	return &productRepository{
		// db: db,
	}
}

func (r *productRepository) GetAll(ctx context.Context) ([]model.Product, error) {
	// Simulate database call
	var allProducts []model.Product
	for _, product := range productsStore {
		allProducts = append(allProducts, product)
	}
	return allProducts, nil
}

func (r *productRepository) GetByID(ctx context.Context, id string) (*model.Product, error) {
	// Simulate database call
	product, ok := productsStore[id]
	if !ok {
		return nil, ErrNotFound
	}
	return &product, nil
}

func (r *productRepository) Create(ctx context.Context, product *model.Product) (*model.Product, error) {
	// Simulate database call
	if _, exists := productsStore[product.ID]; exists {
		return nil, fmt.Errorf("product with ID %s already exists", product.ID)
	}
	productsStore[product.ID] = *product
	return product, nil
}

func (r *productRepository) Update(ctx context.Context, product *model.Product) (*model.Product, error) {
	// Simulate database call
	if _, exists := productsStore[product.ID]; !exists {
		return nil, ErrNotFound
	}
	productsStore[product.ID] = *product
	return product, nil
}

func (r *productRepository) Delete(ctx context.Context, id string) error {
	// Simulate database call
	if _, exists := productsStore[id]; !exists {
		return ErrNotFound
	}
	delete(productsStore, id)
	return nil
}
