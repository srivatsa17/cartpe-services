cartBaseUrl = 'api/v1/cart'

routes = [
    cartBaseUrl + '',               # Add/Edit/Empty items from cart
    cartBaseUrl + '/<id>',          # Update/Delete items from cart
]