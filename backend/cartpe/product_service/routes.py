productsBaseUrl = 'api/v1/products'
routes = [
    # Products model
    productsBaseUrl + '',                                       # Get all products or Create a product
    productsBaseUrl + '/<id>',                                  # Get/Update/Delete a particular product

    # Product categories model
    productsBaseUrl + '/categories',                            # Get all product categories or Create a product category
    productsBaseUrl + '/categories/<id>',                       # Get/Update/Delete a particular product category

    # Product reviews model
    productsBaseUrl + '/reviews?product=<id>',                   # Get all reviews for a product or Create one
    productsBaseUrl + '/reviews?product=<id>&review=<id>',       # Get/Update/Delete a particular review for a product 

    # Product images model
    productsBaseUrl + '/images?product=<id>',                    # Get all images for a product or Create one
    productsBaseUrl + '/images/?product=<id>&image=<id>',        # Get/Update/Delete a particular image for a product

    # Product discounts model
    productsBaseUrl + '/discounts?product=<id>',                 # Get all discounts for a product or Create one
    productsBaseUrl + '/discounts?product=<id>&discount=<id>',   # Get/Update/Delete a particular discount for a product 
]