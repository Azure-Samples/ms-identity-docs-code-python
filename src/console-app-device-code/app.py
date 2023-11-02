"""
A Python application that demonstrates how to use the
Device Code flow to make an API call to Microsoft Graph.
"""

# Microsoft Authentication Library (MSAL) for Python
import msal

# Used to allow the app to make the HTTP request to Graph
import requests

# MSAL configs
config = {
    # Full directory URL, in the form of https://login.microsoftonline.com/<tenant_id>
    "authority": "https://login.microsoftonline.com/Enter_the_Tenant_ID_Here",
    # 'Application (client) ID' of app registration in the Microsoft Entra admin center - this value is a GUID
    "client_id": "Enter_the_Application_Id_Here",
}

# Create a MSAL public client application
msalClientApp = msal.PublicClientApplication(
    config["client_id"], authority=config["authority"]
)

# Initialize the Device Code flow for the necessary scope(s)
deviceFlow = msalClientApp.initiate_device_flow(scopes=["User.Read"])

# Displays a message instructing the user to authenticate via their browser
print(deviceFlow["message"], flush=True)

# Get the Graph access token from MSAL
msalResponse = msalClientApp.acquire_token_by_device_flow(deviceFlow)

if "access_token" in msalResponse:
    # Make an HTTP GET request to the Graph API using the access token and display the response
    print(
        requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": "Bearer " + msalResponse["access_token"]},
        ).json()
    )
