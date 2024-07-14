shippingAddressBaseUrl = "api/v1/shipping"

routes = [
    shippingAddressBaseUrl + "/countries",  # Add/Get countries
    shippingAddressBaseUrl + "/address",  # Add/Get address with locality details
    shippingAddressBaseUrl + "/user-address",  # Add/Get user address with additional details
    shippingAddressBaseUrl + "/user-address/<id>",  # Get/Update/Delete user address
]
