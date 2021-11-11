"""
This application represents a confidential client application that is going to be
calling Microsoft Graph as itself. This is a confidential client in that the
application will need its own identity and security token to perform the work, and
it is not doing this on behalf of an enterprise user.

An example of this might be a nightly script that runs a query against a database,
and based on the results sends an email to multiple people in the organization.
"""
import sys
import requests
import json

from click import command, option
from msal import ConfidentialClientApplication

@command()
@option('-t', '--tenant', type=str, required=True, prompt='Enter the tenent name or id (GUID) in which this application was regsitered. E.g. contoso.onmicrosoft.com', help='Either the "Primary domain" or "Tenant ID" for the Azure Active Directory instance this application was registered in. E.g. contoso.onmicrosoft.com')
@option('-c', '--client-id', type=str, required=True, prompt='Enter this application\'s client id', help='The "Application (client) ID" (GUID) found in this application\'s app registration in Azure Active Directory.')
@option('-o', '--object-id', type=str, required=True, prompt='Enter this application\'s object id', help='The "Object ID" (GUID) found in this application\'s app registration in Azure Active Directory.')
@option('-s', '--secret', type=str, required=True, prompt='Enter the application\'s secret', hide_input=True, help='Any of the non-expired "Client secrets" value found in this application\'s app registration in Azure Active Directory.')
def main(tenant: str, client_id: str, object_id: str, secret: str):
    """Example of MSAL for Python usage."""

    authority = f'https://login.microsoft.com/{tenant}' # https://login.microsoft.com/contoso.onmicrosoft.com or https://login.microsoft.com/6ad988bf-86f1-61af-31ab-6d7cd011db46

    # This app instance should be a long-lived instance, as it maintains
    # its own in-memory token cache (by default)
    app = ConfidentialClientApplication(client_id=client_id, authority=authority, app_name='docs-msal-py-cli',
                                        client_credential=secret)

    # Always first check for an existing token in the cache (and/or refresh if needed)
    result : dict[str, any] = app.acquire_token_silent(scopes=['https://graph.microsoft.com/.default'], account=None)

    # If token could not be found in the cache or could not be refreshed, then aquire a new token
    if not result:
        result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

        print('Could not find a cached token, so fetching a new one.')
    
    if 'access_token' in result:
        # Get this app registration's information
        response = requests.get(f'https://graph.microsoft.com/v1.0/applications/{object_id}', headers={'Authorization': f'Bearer {result["access_token"]}'}).json()
        print(f'Graph API call result: {json.dumps(response, indent=2)}')
    
    else:
        print(f"A \"{result.get('error')}\" error was encountered by retrieving an access token.")
        print(result.get('error_description'))
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())