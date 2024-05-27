import requests
from cartpe import settings
from django.core.exceptions import ValidationError

"""
The following Google API's returns the following attributes as part of the json response.
1.  API - https://oauth2.googleapis.com/token
    Request method - POST.
    Request body - code, redirect_uri.
    Response body - access_token, expires_in, scope, token_type, id_token
2.  API - https://www.googleapis.com/oauth2/v3/tokeninfo
    Request method - GET.
    Query params - access_token.
    Response body - azp, aud, sub, scope, exp, expires_in, email, email_verified, access_type.
3.  API - https://www.googleapis.com/oauth2/v3/userinfo
    Request method - GET.
    Query params - access_token.
    Response body - sub, name, given_name, family_name, picture, email, email_verified, locale.
"""

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class GoogleLogin():
    """
    1. The client gets and sends a `code` upon clicking the google account with which they want to login with.
    The serializer sends the `code` and `redirect_uri` to `get_google_access_token`.
    2. The Google API - https://oauth2.googleapis.com/token is used to get an access token upon `POST` request.
    3. The Google API - https://www.googleapis.com/oauth2/v3/userinfo along with the obtained `access_token` is used to \
    obtain user details upon `GET` request.
    4. The db is checked if user with the obtained email exists or not. If yes, we pass the user details along with \
    tokens just like normal login flow. Else, we register the user in db and then pass on the tokens and user details.
    """
    def get_google_access_token(self, code, redirect_uri):
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }

        response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        
        if not response.ok:
            raise ValidationError(response.json())

        if "access_token" not in response.json():
            raise ValidationError("Unable to fetch access token from Google response.")

        return response.json()["access_token"]

    def get_google_user_info(self, access_token = None):
        if not access_token:
            raise ValidationError("Field access_token is required.")
    
        params = { "access_token": access_token }
        response = requests.get(GOOGLE_USER_INFO_URL, params)

        if not response.ok:
            raise ValidationError("Failed to obtain user info from Google.")

        return response.json()

google_api_client = GoogleLogin()