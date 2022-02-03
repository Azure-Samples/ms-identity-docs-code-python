"""
This application represents a confidential client application that is going to
be calling Microsoft Graph as itself. This is a confidential client in that the
application will need its own identity and security token to perform the work,
and it is not doing this on behalf of an enterprise user.

An example of this might be a nightly script that runs a query against a
database, and based on the results sends an email to multiple people in the
organization.
"""
import json
import requests

# <ms_docref_import_modules>
from msal import ConfidentialClientApplication

# </ms_docref_import_modules>

# MSAL configs
# <ms_docref_configure_msal>
config = {
    # Full directory URL, in the form of https://login.microsoftonline.com/<tenant>
    "authority": "",
    # 'Application (client) ID' of app registration in Azure portal - this value is a GUID
    "client_id": "",
    # Client secret 'Value' (not its ID) from 'Client secrets' in app registration in Azure portal
    "client_secret": "",
    # Client 'Object ID' of app registration in Azure portal - this value is a GUID
    "client_objectid": "",
}
# </ms_docref_configure_msal>

# This app instance should be a long-lived instance, as it maintains
# its own in-memory token cache (by default)
# <ms_docref_create_app_instance>
app = ConfidentialClientApplication(
    client_id=config["client_id"],
    authority=config["authority"],
    client_credential=config["client_secret"],
)
# </ms_docref_create_app_instance>

# First check for an existing token in the cache and/or refresh if needed
# <ms_docref_get_graph_token>
result = app.acquire_token_silent(
    scopes=["https://graph.microsoft.com/.default"], account=None
)

# If token could not be found in the cache or could not be refreshed, then
# acquire a new token
if not result:
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    print("Could not find a cached token, so fetching a new one.")
# </ms_docref_get_graph_token>
# <ms_docref_make_graph_call>
if "access_token" in result:
    # Get this app registration's information
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/applications/{config['client_objectid']}",
        headers={"Authorization": f'Bearer {result["access_token"]}'},
    ).json()
    print(f"Graph API call result: {json.dumps(response, indent=2)}")

else:
    print("Error encountered when requesting access token: " f"{result.get('error')}")
    print(result.get("error_description"))
# </ms_docref_make_graph_call>
