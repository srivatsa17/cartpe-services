productsBaseUrl = 'api/v1/products'
routes = [
    # Products model
    productsBaseUrl + '',                                       # Get all products
    productsBaseUrl + '/create',                                # Create a product
    productsBaseUrl + '/<id>',                                  # Get a particular product
    productsBaseUrl + '/update/<id>',                           # Update a particular product
    productsBaseUrl + '/delete/<id>',                           # Delete a particular product

    # Product categories model
    productsBaseUrl + '/categories',                            # Get all product categories
    productsBaseUrl + '/categories/<id>',                       # Get a particular product category
    productsBaseUrl + '/categories/create',                     # Create a product category
    productsBaseUrl + '/categories/update/<id>',                # Update a product category
    productsBaseUrl + '/categories/delete/<id>',                # Delete a product category

    # Product reviews model
    productsBaseUrl + '/<id>/reviews',                           # Get all reviews for a product 
    productsBaseUrl + '/<id>/reviews/<review-id>',               # Get a particular review for a product 
    productsBaseUrl + '/<id>/reviews/create',                    # Create a reviews for a product 
    productsBaseUrl + '/<id>/reviews/update/<review-id>',        # Update a review for a product 
    productsBaseUrl + '/<id>/reviews/delete/<review-id>',        # Delete a review for a product 

    # Product images model
    productsBaseUrl + '/<id>/images/',                           # Get all images for a product 
    productsBaseUrl + '/<id>/images/<image-id>',                 # Get a particular images for a product 
    productsBaseUrl + '/<id>/images/create',                     # Upload an image for a product 
    productsBaseUrl + '/<id>/images/update/<image-id>',          # Update an image for a product 
    productsBaseUrl + '/<id>/images/delete/<image-id>',          # Delete an image for a product   

    # Product discounts model
    productsBaseUrl + '/<id>/discounts/',                        # Get all discounts for a product 
    productsBaseUrl + '/<id>/discounts/<discount-id>',           # Get a particular discount for a product 
    productsBaseUrl + '/<id>/discounts/create',                  # Create a discounts for a product 
    productsBaseUrl + '/<id>/discounts/update/<discount-id>',    # Update a discount for a product 
    productsBaseUrl + '/<id>/discounts/delete/<discount-id>',    # Delete a discount for a product 
]