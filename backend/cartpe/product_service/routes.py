productsBaseUrl = 'api/v1/products'
routes = [
    # Products model
    productsBaseUrl + '',                                   # Get all products or Create one
    productsBaseUrl + '/<id>',                              # Get/Update/Delete a particular product

    # Product categories model
    productsBaseUrl + '/categories',                        # Get all product categories or Create one
    productsBaseUrl + '/categories/<id>',                   # Get/Update/Delete a particular product category

    # Product brands model
    productsBaseUrl + '/brands',                            # Get all product brands or Create one
    productsBaseUrl + '/brands/<id>',                       # Get/Update/Delete a particular product brand

    # Product images model
    productsBaseUrl + '/images?product=<id>',               # Get all images for a product or Create one
    productsBaseUrl + '/images/<id>',                       # Get/Update/Delete a particular image

    # Product reviews model
    productsBaseUrl + '/reviews?product=<id>',              # Get all reviews for a product or Create one
    productsBaseUrl + '/reviews/<id>',                      # Get/Update/Delete a particular review for a product
]