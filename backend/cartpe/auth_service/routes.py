authBaseUrl = "api/v1/users"

routes = [
    authBaseUrl + "/register",  # Create a user
    authBaseUrl + "/register-google",  # Create a user using Google OAuth
    authBaseUrl + "/verify-email",  # Verify email for a user
    authBaseUrl + "/login",  # Login a user
    authBaseUrl + "/google-login",  # Login a user using Google OAuth
    authBaseUrl + "/token/refresh",  # Get fresh access token using refresh token
    authBaseUrl + "/logout",  # Logout a user
    authBaseUrl + "/change-password",  # Change password
    authBaseUrl + "/deactivate",  # Deactivate user account
    authBaseUrl + "/edit-profile",  # Edit or get user profile
    authBaseUrl + "/reset-password",  # Request for reset password
    authBaseUrl + "/reset-password-confirm",  # Reset password with new password
]
