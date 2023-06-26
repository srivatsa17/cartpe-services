authBaseUrl = 'api/v1/users'
routes = [
    authBaseUrl + '/register',              # Create a user[POST]
    authBaseUrl + '/verify-email',          # Verify email for a user[PATCH]
    authBaseUrl + '/login',                 # Login a user[POST]
    authBaseUrl + '/token/refresh',         # Get fresh access token using refresh token[POST]
    authBaseUrl + '/logout',                # Logout a user[POST]
    authBaseUrl + '/change-password',       # Change password for user[POST]
    authBaseUrl + '/reset-password',        # Reset password for user[POST]
    authBaseUrl + '/<id>'                   # Get user details[GET]
]