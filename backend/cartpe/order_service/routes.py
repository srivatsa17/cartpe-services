orderBaseUrl = "api/v1/orders"

routes = [
    orderBaseUrl + "/razorpay",  # Create an order in razorpay
    orderBaseUrl + "",  # Get/Create an order
    orderBaseUrl + "/<id>",  # Get/Update/Delete an order
]
