# -*- coding: utf-8 -*-

"""
A Python Flask application that contains various user routes with different
protection levels using the Microsoft Authentication Library (MSAL) for Python.

Note: This example does NOT use the Flask adapter found at
https://github.com/azure-samples/ms-identity-python-samples-common, however
you should consider wrapping the common auth logic presented here into your
own similar module.

Additionally, consider integrating your session tracking with Flask-Login and
Flask-Principal for a more robust user session experience. This sample exists
to show very direct MSAL usage, not how to obfuscate its usage into various
common Flask constructs.

See also:
https://github.com/Azure-Samples/ms-identity-python-webapp
https://github.com/AzureAD/microsoft-authentication-extensions-for-python
"""

from typing import Any

# Used to make an http request to graph
import requests

# <ms_docref_import_msal>
# Import Microsoft Authentication Library (MSAL) for Python
import msal
from msal.authority import (AuthorityBuilder, AZURE_PUBLIC)
# </ms_docref_import_msal>

# <ms_docref_import_modules>
# Flask imports to handle render templates and session access
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import Forbidden, Unauthorized
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
# </ms_docref_import_modules>

# <ms_docref_create_and_initialize_app>
def create_app():
    """Configure the flask application"""

    # Initialize the flask app
    app = Flask(__name__)

    # Load Flask configuration settings such as session configs
    app.config.from_object("default_settings")

    # Initialize the serverside session for the app to cordinate auth flows, store the 
    # "user" object and store MSAL client caches (token cache and http cache)
    Session(app)

    # Support both http (localhost) and https (deployed behind a web
    # proxy such as in most cloud deployments). See:
    # https://flask.palletsprojects.com/en/2.0.x/deploying/wsgi-standalone/#proxy-setups
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
   # </ms_docref_create_and_initialize_app>

    # If a user attempts to navigate to any place in the application that
    # raises an Unauthorized error, this error handler will immediately
    # redirect the user through the auth code flow which will then get
    # them signed in and back to where they were initially headed. This
    # user experience is optional. As an alternative, the user could be
    # presented with a sign-in page/link and the user can kick off the
    # auth code flow manually.

    # <ms_docref_build_auth_code_flow>
    # Redirect unauthorized users through the auth code flow to sign in
    @app.errorhandler(Unauthorized)
    def initiate_auth_code_flow(error):
        """
        Builds the auth code flow and then redirects to Azure AD to allow the
        user to perform authorization.
        """

        # Remove stale user from session data (if any)
        session.pop("user", None)

        # The MSAL ConfidentialClientApplication will always make an HTTP
        # request to the metadata endpoint for your tenant upon creation.
        # Using the http cache feature will optimize that process as that
        # data is highly cacheable, and ideally would survive for the whole
        # user's session. This shouldn't be cached across user sessions.
        http_cache: dict = session.get("msal_http_response_cache", {})

        # The MSAL client has a method to initiate the auth code flow, so the
        # first step is to create a MSAL client. This client doesn't need
        # a token_cache as none of the interactions with it use or produce
        # tokens in the initiate_auth_code_flow process.
        msal_client = msal.ConfidentialClientApplication(
            app.config.get("CLIENT_ID"),
            authority=AuthorityBuilder(AZURE_PUBLIC, app.config.get("TENANT_ID")),
            http_cache=http_cache,
        )

        # Use the MSAL client to build the auth code flow dictionary.
        # We are asking for the user to consent to all scopes that will be used
        # in this application up front. Alternatively, you could provide no
        # scopes and do step-up authentication as necessary.
        auth_code_flow: "dict[str, Any]" = msal_client.initiate_auth_code_flow(
            scopes=["https://graph.microsoft.com/User.Read"],
            redirect_uri=url_for("authorized", _external=True),
        )

        # Add a dictionary entry to store where the user should be directed to
        # after the last leg of the auth code flow
        auth_code_flow["post_sign_in_url"] = request.url_rule.rule

        # Add the auth code flow initiation to the session
        session["auth_code_flow"] = auth_code_flow

        # Update the session's MSAL http response cache
        session["msal_http_response_cache"] = http_cache

        # Redirect to Azure AD to allow the user to perform any auth steps
        # required. This could be logging in (if not already signed in) and
        # agreeing to the consent form. After this is complete, Azure AD will
        # redirect back to this application.
        return redirect(session["auth_code_flow"]["auth_uri"])
    # </ms_docref_build_auth_code_flow>

    #### Application routes are defined below this point ####
    
    # <ms_docref_unprotected_app_route>
    @app.get("/")
    # This route does not require any authentication or authorization
    def index():

        # Return the "Index" view
        return render_template("public/index.html")

    @app.get("/auth/redirect")
    # This route does not require any authentication or authorization and is not
    # called directly by the user but instead Azure AD will redirect the user back
    # to this URL after their sign-in is complete.
    def authorized():
        """
        Handles the redirect from Azure AD for the second leg of the auth code flow.
        """

        # After the user signs in and accepts the required application
        # permissions, Azure AD will redirect the user back to this route, and
        # you need to capture the returned id token (which acts as the "User"
        # in this context) and exchange the id token for the application's
        # required access & refresh tokens.

        # There is no "View" here, instead the user's browser will be
        # redirected to the protected URL they were attempting to visit in the
        # first place.

        # Pop out the auth code flow in which we started in their prior call
        # as it isn't needed that after this request is complete.
        auth_code_flow: "dict[str, Any]" = session.pop("auth_code_flow")

        # Hydrate the existing MSAL token cache from the session or start an
        # empty one.
        token_cache = msal.SerializableTokenCache()
        if session.get("token_cache"):
            token_cache.deserialize(session["token_cache"])

        # The MSAL ConfidentialClientApplication will always make an HTTP
        # request to the metadata endpoint for your tenant upon creation.
        # Using the http cache feature will optimize that process as that
        # data is highly cacheable, and ideally would survive for the whole
        # user's session. This shouldn't be cached across user sessions.
        http_cache: dict = session.get("msal_http_response_cache", {})

        msal_client = msal.ConfidentialClientApplication(
            app.config.get("CLIENT_ID"),
            authority=AuthorityBuilder(AZURE_PUBLIC, app.config.get("TENANT_ID")),
            client_credential=app.config.get("CLIENT_CREDENTIAL"),
            token_cache=token_cache,
            http_cache=http_cache,
        )

        # Exchange the original auth code flow request and the new Azure AD
        # response parameters for id, access, and refresh tokens based on the
        # requested scopes from the original request.
        result: "dict[str, Any]" = msal_client.acquire_token_by_auth_code_flow(
            auth_code_flow, request.args
        )

        # Persist the MSAL client caches in the user's session for future
        # calls to acquire_token_silently.
        session["token_cache"] = token_cache.serialize()
        session["msal_http_response_cache"] = http_cache

        # Our "user" session object will contain both the raw ID token and the
        # deserialized claims. This supports easy access to the claims and
        # easy access to check if the id_token is still valid (not expired,
        # for example)
        session["user"] = {
            "id_token": result["id_token"],
            "id_token_claims": result["id_token_claims"],
        }

        # Send the user to their original destination, which was captured in
        # the auth_code_flow session object.
        return redirect(auth_code_flow["post_sign_in_url"])
    # </ms_docref_unprotected_app_route>
    
    # <ms_docref_require_authentication>
    @app.get("/graph")
    # This route requires prior authentication
    def graph():
        # If the session doesn't currently contain a "user" entry or is missing
        # the token cache entry, that means we haven't completed the auth code
        # flow yet. Raise an Unauthorized error, which can be used to trigger a
        # new auth code flow.
        if not session.get("user") or not session.get("token_cache"):
            raise Unauthorized()

        # Perform additional session validation (as desired). For example, this
        # checks to ensure that id_token isn't expired. Azure AD tokens, by
        # default, are valid for 1 hour (but can be configured as low as 10
        # minutes or as much as 1 day). Raise an Unauthorized error, which can
        # be used to trigger a new auth code flow.
        try:
            msal.oauth2cli.oidc.decode_id_token(session["user"]["id_token"])
        except RuntimeError as err:
            raise Unauthorized("ID Token expired or invalid") from err

        # Perform a request to graph that only requires User.Read scope
        # This scope was already requested to be granted by the user.

        # Get an access token that contains the necessary scope for User.Read
        # on graph. This token will come from the cache (and if expired, will
        # use the refresh token found in the cache to fetch and cache a new
        # token.

        # In order to get a token, it either needs to be in the cache or the
        # cache needs a valid refresh token for that scope. So the first step
        # is to load the token cache from the session. This is the same token
        # cache that was used when the id token was exchanged for access
        # tokens in the last leg of the auth code flow.
        token_cache = msal.SerializableTokenCache()
        token_cache.deserialize(session["token_cache"])

        # The MSAL ConfidentialClientApplication will always make an HTTP
        # request to the metadata endpoint for your tenant upon creation.
        # Using the http cache feature will optimize that process as that
        # data is highly cacheable, and ideally would survive for the whole
        # user's session. This shouldn't be cached across user sessions.
        http_cache: dict = session.get("msal_http_response_cache", {})
    # </ms_docref_require_authentication>

        # <ms_docref_configure_app>
        # Create an MSAL client using the app's configuration values and provide
        # the token cache.
        msal_client = msal.ConfidentialClientApplication(
            app.config.get("CLIENT_ID"),
            authority=AuthorityBuilder(AZURE_PUBLIC, app.config.get("TENANT_ID")),
            client_credential=app.config.get("CLIENT_CREDENTIAL"),
            token_cache=token_cache,
            http_cache=http_cache,
        )
        # </ms_docref_configure_app>

        # <ms_docref_acquire_token>
        # Invoke the acquire_token flow on the MSAL client for the requested
        # account and scope. Look for and retrieve an existing valid token in
        # the cache or use the refresh token to fetch a new access token.
        result: "dict[str: Any]" = msal_client.acquire_token_silent(
            scopes=["https://graph.microsoft.com/User.Read"],
            account=msal_client.get_accounts()[0],
        )

        # Update the session's token cache to reflect the new access token and
        # refresh token.
        if token_cache.has_state_changed:
            session["token_cache"] = token_cache.serialize()
        session["msal_http_response_cache"] = http_cache
        # </ms_docref_acquire_token>

        # If 'result' comes back with an error, that means that the user will
        # need to go through the auth grant flow again, as the tokens in the
        # cache cannot be used to make this request for some reason. How you
        # handle this situation will depend on your desired user experience.
        # Furthermore, in this sample we asked for all app permissions up
        # front but in reality we could have asked for no specific scopes in
        # the initial auth code flow exchange and performed on-demand, step-up
        # authentication when reaching this based on the MSAL token cache
        # contents.

        # <ms_docref_call_ms_graph>
        # Simple HTTP Get to graph showing the usage of the retrieved access token
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {result['access_token']}"},
        ).json()

        # Show the "Graph" view for authenticated users
        return render_template("authenticated/graph.html", 
            graphCallResponse=response,
            graphAccessTokenExpiresInSeconds=result['expires_in'])
        # </ms_docref_call_ms_graph>

    # <ms_docref_require_admin_role_authNZ>
    # This route requires prior authentication and authorization. 
    # Users should have the application-defined, admin role assigned.
    @app.get("/admin")
    def admin():
        # If the session doesn't currently contain a "user" entry that means we
        # haven't completed the auth code flow yet. Raise an Unauthorized error,
        # which can be used to trigger a new auth code flow.
        if not session.get("user"):
            raise Unauthorized()

        # Perform additional session validation (as desired). For example, this
        # checks to ensure that id_token isn't expired. Azure AD tokens, by
        # default, are valid for 1 hour (but can be configured as low as 10
        # minutes or as much as 1 day). Raise an Unauthorized error, which can
        # be used to trigger a new auth code flow.
        try:
            msal.oauth2cli.oidc.decode_id_token(session["user"]["id_token"])
        except RuntimeError as err:
            raise Unauthorized("ID Token expired or invalid.") from err

        # If a role check was requested, look at the user's claims for the "roles"
        # claim. If the claim doesn't exist or does not contain "admin" as an item
        # in it, then raise a Forbidden error.
        user_claims = session["user"]["id_token_claims"]
        if "roles" not in user_claims or "admin" not in user_claims["roles"]:
            raise Forbidden("User is missing a required role.")
    # </ms_docref_require_admin_role_authNZ>

    # <ms_docref_display_admin_view_content>
        # Upon successful authentication, show the "Admin" view
        return render_template(
            "authenticated/admin.html", graphCallResponse=user_claims
        )
    # </ms_docref_display_admin_view_content>

    # <ms_docref_logout_user>
    @app.get("/logout")
    def logout():
        # If we had anything in our session tied to auth, completely remove it.
        # The msal_http_response_cache can survive this as there is nothing
        # related to an individual authentication cached in there.
        session.pop("user", None)
        session.pop("auth_code_flow", None)
        session.pop("token_cache", None)

        # If your application supported logging in with multiple accounts and
        # you could selectively log out of individual accounts, then instead
        # of removing the token_cache from the session, you'd hydrate the
        # MSAL client with the token_cache from the session and then call
        # msal_client.remove_account(_account_to_remove_), then persist that
        # updated token_cache back to the session.

        # If you also wanted your app's log out to suggest that the user logs
        # out of their Azure AD SSO session as well, you would redirect the
        # user as such:
        # return redirect(f"{AuthorityBuilder(AZURE_PUBLIC, app.config.get("TENANT_ID")}"
        #   "/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('index', _external=True)}")
        # If you do not do that, the user will still be signed into Azure AD
        # (SSO), meaning next time the user needs to sign in here, it will
        # happen without the user needing to re-enter their credentials.
        return redirect(url_for("index"))

    return app
    # </ms_docref_logout_user>
