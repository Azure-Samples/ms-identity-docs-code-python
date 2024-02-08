# <ms_docref_script_intro_comment>
"""
This application represents a confidential client application that is going to
be calling Microsoft Graph as itself. This is a confidential client in that the
application will need its own identity and security token to perform the work,
and it is not doing this on behalf of an enterprise user.

An example of this might be a nightly script that runs a query against a
database, and based on the results sends an email to multiple people in the
organization.
"""
# </ms_docref_script_intro_comment>
import json
import requests

# <ms_docref_import_modules>
# Import the required MSAL for Python module(s)
from msal import ConfidentialClientApplication
# </ms_docref_import_modules>

# <ms_docref_configure_msal>
# MSAL requires these values for interaction with the Microsoft identity platform.
# Get the values from the Microsoft Entra admin center > Identity > Applications > App registrations > $YOUR_APP_NAME.
config = {
    # Full directory URL, in the form of https://login.microsoftonline.com/<tenant_id>
    "authority": "https://login.microsoftonline.com/Enter_the_Tenant_ID_Here",
    # 'Application (client) ID' of app registration in the Microsoft Entra admin center - this value is a GUID
    "client_id": "Enter_the_Application_Id_Here",
    # Client secret 'Value' (not its ID) from 'Client secrets' in the Microsoft Entra admin center
    "client_secret": "Enter_the_Client_Secret_Value_Here",
    # Client 'Object ID' of app registration in the Microsoft Entra admin center - this value is a GUID
    "client_objectid": "Enter_the_Client_Object_ID_Here",
}
# </ms_docref_configure_msal>

# <ms_docref_create_app_instance>
# This app instance should be a long-lived instance because
# it maintains its own in-memory token cache (the default).
app = ConfidentialClientApplication(
    client_id=config["client_id"],
    authority=config["authority"],
    client_credential=config["client_secret"],
)
# </ms_docref_create_app_instance>

# <ms_docref_get_graph_token>
# First, check for a token in the cache, refreshing it if needed
result = app.acquire_token_silent(
    scopes=["https://graph.microsoft.com/.default"], account=None
)

# If no token was found in the cache or the token refresh failed, get a new one
if not result:
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    print("Could not find a cached token, so fetching a new one.")
# </ms_docref_get_graph_token>

# <ms_docref_make_graph_call>
if "access_token" in result:
    # Get *this* application's application object from Microsoft Graph
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/applications/{config['client_objectid']}",
        headers={"Authorization": f'Bearer {result["access_token"]}'},
    ).json()
    print(f"Graph API call result: {json.dumps(response, indent=2)}")

else:
    print("Error encountered when requesting access token: " f"{result.get('error')}")
    print(result.get("error_description"))
# </ms_docref_make_graph_call>
