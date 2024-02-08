"""
This is an Azure Function that responds at GET /api/greeting.

Using the built-in authentication and authorization capabilities (sometimes
referred to as "Easy Auth") of Azure Functions, offloads part of the authentication
and authorization process by ensuring that every request to this Azure Function has
an access token. That access token has had its signature, issuer (iss), expiry
dates (exp, nbf), and audience (aud) validated. This means all that is left to
perform is any per-function authorization related to your application.
"""

import jwt

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /api/greeting
    Scope Required: Greeting.Read
    """

    # Extract the access token from the Authorization header
    # Authorization: Bearer <access_token>
    access_token: str = req.headers["authorization"].split(" ")[1]

    # Because Easy Auth has already validated the signature, the validation is not
    # performed again, but instead the token is is being decoded only to get access
    # to its contained scopes claim.
    try:
        scopes: str = jwt.decode(
            access_token, options={"verify_signature": False, "require": ["scp"]}
        )["scp"]
    except jwt.PyJWTError:
        return func.HttpResponse("Bearer token not valid.", status_code=403)

    # This API endpoint requires the "Greeting.Read" scope to be present, if it is
    # not, then reject the request with a 403.
    if "Greeting.Read" not in scopes.split(" "):
        return func.HttpResponse("Missing required scope.", status_code=403)

    # Authentication is complete, process request.
    return func.HttpResponse(
        "Hello, world. You were able to access this because you provided a valid "
        "access token with the Greeting.Read scope as a claim.",
        status_code=200,
    )
