package handler

import (
	"context"
	"errors"
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/your-username/echo-api/internal/model"
	"github.com/your-username/echo-api/internal/service"
)

type ProductHandler struct {
	productService service.ProductService
}

func NewProductHandler(productService service.ProductService) *ProductHandler {
	return &ProductHandler{
		productService: productService,
	}
}

// @Summary Get all products
// @Description Get a list of all products
// @Tags Product
// @Accept json
// @Produce json
// @Success 200 {array} model.Product
// @Failure 500 {object} map[string]string
// @Router /products [get]
func (h *ProductHandler) GetProducts(c echo.Context) error {
	ctx := c.Request().Context()
	products, err := h.productService.GetAllProducts(ctx)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, products)
}

// @Summary Get a product by ID
// @Description Get a single product by its ID
// @Tags Product
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 200 {object} model.Product
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /products/{id} [get]
func (h *ProductHandler) GetProductByID(c echo.Context) error {
	id := c.Param("id")
	ctx := c.Request().Context()
	product, err := h.productService.GetProductByID(ctx, id)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) { // Assuming ErrNotFound is a custom error from service
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Product not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, product)
}

// @Summary Create a new product
// @Description Create a new product with the provided data
// @Tags Product
// @Accept json
// @Produce json
// @Param product body model.Product true "Resource object to create"
// @Success 201 {object} model.Product
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /products [post]
func (h *ProductHandler) CreateProduct(c echo.Context) error {
	var product model.Product
	if err := c.Bind(&product); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
	}

	ctx := c.Request().Context()
	createdProduct, err := h.productService.CreateProduct(ctx, &product)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusCreated, createdProduct)
}

// @Summary Update an existing product
// @Description Update a product by ID with the provided data
// @Tags Product
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Param product body model.Product true "Resource object to update"
// @Success 200 {object} model.Product
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /products/{id} [put]
func (h *ProductHandler) UpdateProduct(c echo.Context) error {
	id := c.Param("id")
	var product model.Product
	if err := c.Bind(&product); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
	}
	product.ID = id // Ensure ID from path is used

	ctx := c.Request().Context()
	updatedProduct, err := h.productService.UpdateProduct(ctx, &product)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Product not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, updatedProduct)
}

// @Summary Delete a product
// @Description Delete a product by its ID
// @Tags Product
// @Accept json
// @Produce json
// @Param id path string true "Resource ID"
// @Success 204 "No Content"
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /products/{id} [delete]
func (h *ProductHandler) DeleteProduct(c echo.Context) error {
	id := c.Param("id")
	ctx := c.Request().Context()
	err := h.productService.DeleteProduct(ctx, id)
	if err != nil {
		if errors.Is(err, service.ErrNotFound) {
			return c.JSON(http.StatusNotFound, map[string]string{"error": "Product not found"})
		}
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.NoContent(http.StatusNoContent)
}
