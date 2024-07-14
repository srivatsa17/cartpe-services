productsBaseUrl = "/api/v1/products"
routes = [
    # Products model
    productsBaseUrl + "",  # Get all products or Create one
    productsBaseUrl + "/<id>",  # Get/Update/Delete a particular product
    # Product categories model
    productsBaseUrl + "/categories",  # Get all product categories or Create one
    productsBaseUrl + "/categories/<id>",  # Get/Update/Delete a particular product category
    productsBaseUrl
    + "/categories/search",  # Get a list of related product categories based on a search
    # Product brands model
    productsBaseUrl + "/brands",  # Get all product brands or Create one
    productsBaseUrl + "/brands/<id>",  # Get/Update/Delete a particular product brand
    # Product Wishlist model
    productsBaseUrl + "/wishlist",  # Get all user product wishlist or Create one
    productsBaseUrl + "/wishlist/<id>",  # Get/Update/Delete a particular user product wishlist
    # Product reviews model
    productsBaseUrl + "/<product_id>/reviews",  # Get a product review or Create one
    productsBaseUrl
    + "/<product_id>/reviews/<id>",  # Get/Update/Delete a particular review for a product
]
