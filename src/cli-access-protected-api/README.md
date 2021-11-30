<!-- Updated, but leaving commented out until we're ready to ship in samples browser
---
# Metadata required by https://docs.microsoft.com/samples/browse/
# Metadata properties: https://review.docs.microsoft.com/help/contribute/samples/process/onboarding?branch=main#add-metadata-to-readme
languages:
- python
page_type: sample
name: Python console application that accesses a protected API
description: This a Python console application that accesses a protected API. The code in this sample is used by one or more articles on docs.microsoft.com.
products:
- azure
- azure-active-directory
- ms-graph
urlFragment: ms-identity-docs-code-cli-python
---
-->

# Python console application - Access protected API

> This sample application backs one or more technical articles on docs.microsoft.com.

This sample shows how a python console application can access a protected API, as its own identity, using the [Microsoft Autentication Library (MSAL) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python). This scenario supports usages such as cron jobs and also direct command line invocation.

<!-- IMAGE or CONSOLE OUTPUT of running/executed app -->

## Prerequisites

- Python 3.8+
- [Appropriate registered app in Azure Active Directory](https://docs.microsoft.com/azure/active-directory/develop/scenario-daemon-app-registration)

## Running the app (without installing)

Install application runtime dependencies:

```bash
pip install -r dev-requirements.txt
```

Run the application:

```bash
python3 cli.py -t <your-domain>.onmicrosoft.com -c <your-app-client-id> -o <your-app-object-id> -s <a non-expired app secret>
```

Example of the above:

```bash
python3 cli.py -t contoso.onmicrosoft.com -c 714c4653-8063-4a37-83bb-334a7fcfa389 -o cf43d75e-675d-4f3b-9f5e-571fa0922262 -s aVp7Q~CQP_4oSkH~KGDRn.z3X920EipYokQBO
```

```output
Could not find a cached token, so fetching a new one.
Graph API call result: {
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#applications/$entity",
  "id": "cf43d75e-675d-4f3b-9f5e-571fa0922262",
  "deletedDateTime": null,
  "appId": "714c4653-8063-4a37-83bb-334a7fcfa389",
  "createdDateTime": "2021-11-11T20:57:24Z",
  "displayName": "python-cli-app",
  "publisherDomain": "contoso.onmicrosoft.com",
  "signInAudience": "AzureADMyOrg",
  ...
}
```

## Alternative: Running the app (with installation)

Build and install the `msal-py-cli` python module.

```bash
pip install .
```

Run the application:

```bash
msal-py-cli -t <your-domain>.onmicrosoft.com -c <your-app-client-id> -o <your-app-object-id> -s <a non-expired app secret>
```

Uninstall the application:

```bash
pip uninstall msal-py-cli
```

## About the sample app

The python application will use the provided credentials, retrieve a token scoped specifically for the Microsoft Graph API, and will use that token to access it's own application registration information.

<!-- OPTIONAL: Image or ASCII diagram of app and/or auth flow. -->

## Reporting problems

### Sample app not working?

If you can't get the sample working and you've already searched the issues in the sample's repository on GitHub, open an issue in its repo to report the problem.

1. Search the [Issues](https://github.com/Azure-Samples/ms-identity-docs-code-python/issues) in the repository - your problem might already have been reported or have an answer.
1. Nothing similar? [Open an issue](https://github.com/Azure-Samples/ms-identity-docs-code-python/issues/new) that clearly explains the problem you're having running the sample app.

### All other issues

:warning: WARNING: Any issue _not_ limited to running this or another sample app will be closed without being addressed.

For all other requests, see [Support and help options for developers | Microsoft identity platform](https://docs.microsoft.com/azure/active-directory/develop/developer-support-help-options).
