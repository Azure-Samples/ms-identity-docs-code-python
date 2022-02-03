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

# Python | console | protected web API access (Microsoft Graph) | Microsoft identity platform

<!-- Build badges here
![Build passing.](https://img.shields.io/badge/build-passing-brightgreen.svg) ![Code coverage.](https://img.shields.io/badge/coverage-100%25-brightgreen.svg) ![License.](https://img.shields.io/badge/license-MIT-green.svg)
-->

> This sample application backs one or more technical articles on docs.microsoft.com.

This sample shows how a Python console application can access a protected API, as its own identity, using the [Microsoft Autentication Library (MSAL) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python). This scenario supports usages such as cron jobs and also direct command line invocation.

```console
$ python3 cli.py
Could not find a cached token, so fetching a new one.
Graph API call result: {
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#applications/$entity",
  "id": "6ed9c555-6dfd-4f35-b832-f1f634c0b876",
  "deletedDateTime": null,
  "appId": "59c06144-a668-4828-9ca8-ed6e117c8344",
  "applicationTemplateId": null,
  "disabledByMicrosoftStatus": null,
  "createdDateTime": "2021-01-17T15:30:55Z",
  "displayName": "python-cli",
  "description": null,
  "groupMembershipClaims": null,
  ...
}
```

## Prerequisites

- Azure Active Directory (Azure AD) tenant and the permissions or role required for managing app registrations in the tenant.
- Python 3

## Setup

### 1. Register the app

First, complete the steps in [Register an application with the Microsoft identity platform](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app) to register the application.

Use these settings in your app registration.

| App registration <br/> setting   | Value for this sample app                                          | Notes                                                                            |
|:--------------------------------:|:-------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| **Name**                         | `python-cli`                                                       | Suggested value for this sample. <br/> You can change the app name at any time.  |
| **Supported account types**      | **Accounts in this organizational directory only (Single tenant)** | Suggested value for this sample.                                                 |
| **Platform type**                | _None_                                                             | No redirect URI required; don't select a platform.                               |

> :information_source: **Bold text** in the tables above matches (or is similar to) a UI element in the Azure portal, while `code formatting` indicates a value you enter into a text box in the Azure portal.

### 2. Update code sample with app registration values

```python
# Full directory URL, in the form of https://login.microsoftonline.com/<tenant_id>
"authority": "",
# 'Application (client) ID' of app registration in Azure portal - this value is a GUID
"client_id": "",
# Client secret 'Value' (not its ID) from 'Client secrets' in app registration in Azure portal
"client_secret": "",
# Client 'Object ID' of app registration in Azure portal - this value is a GUID
"client_objectid": "",
```

### 3. Install package(s)

To install MSAL libraries:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
python3 cli.py
```

If everything worked, you should receive a response similar to this:

```console
Could not find a cached token, so fetching a new one.
Graph API call result: {
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#applications/$entity",
  "id": "6ed9c555-6dfd-4f35-b832-f1f634c0b876",
  "deletedDateTime": null,
  "appId": "59c06144-a668-4828-9ca8-ed6e117c8344",
  "applicationTemplateId": null,
  "disabledByMicrosoftStatus": null,
  "createdDateTime": "2021-01-17T15:30:55Z",
  "displayName": "python-cli",
  "description": null,
  "groupMembershipClaims": null,
  ...
}
```

## About the code

The python application will use the provided credentials, retrieve a token scoped specifically for the Microsoft Graph API, and will use that token to access it's own application registration information.

## Reporting problems

### Sample app not working?

If you can't get the sample working, you've checked [Stack Overflow](http://stackoverflow.com/questions/tagged/msal), and you've already searched the issues in this sample's repository, open an issue report the problem.

1. Search the [GitHub issues](../../issues) in the repository - your problem might already have been reported or have an answer.
1. Nothing similar? [Open an issue](../../issues/new) that clearly explains the problem you're having running the sample app.

### All other issues

> :warning: WARNING: Any issue in this repository _not_ limited to running one of its sample apps will be closed without being addressed.
For all other requests, see [Support and help options for developers | Microsoft identity platform](https://docs.microsoft.com/azure/active-directory/develop/developer-support-help-options).

## Contributing

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](/CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
