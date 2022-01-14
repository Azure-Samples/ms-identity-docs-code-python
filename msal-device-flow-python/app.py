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
	"authority": "",
	"client_id": "",
	"scopes": ["User.Read"]
}

# Create connection to API via MSAL
msalClientApp = msal.PublicClientApplication(config["client_id"], authority=config["authority"])

# Initialize the Divice Code flow for the desired scope(s)
deviceFlow = msalClientApp.initiate_device_flow(scopes=config["scopes"])

# Displays a message instructing the user to authenticate via their browser
print(deviceFlow["message"], flush=True)

# Get the access token from MSAL
msalResponse = msalClientApp.acquire_token_by_device_flow(deviceFlow)

if "access_token" in msalResponse:
    # Make an HTTP GET request to the Graph API using the access token and display the response
    print(requests.get("https://graph.microsoft.com/v1.0/me", headers={'Authorization': 'Bearer ' + msalResponse['access_token']}).json())
