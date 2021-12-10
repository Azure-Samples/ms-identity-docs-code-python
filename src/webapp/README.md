<!-- Keeping yaml frontmatter commented out for now
---
# Metadata required by https://docs.microsoft.com/samples/browse/
# Metadata properties: https://review.docs.microsoft.com/help/contribute/samples/process/onboarding?branch=main#add-metadata-to-readme
languages:
- python
page_type: sample
name: "Python web application written in Flask that both protects its own endpoints and accesses Microsoft Graph"
description: "This Python web application protects various routes and contacts Microsoft Graph on behalf of the user. The code in this sample is used by one or more articles on docs.microsoft.com."
products:
- azure
- azure-active-directory
- ms-graph
urlFragment: ms-identity-docs-code-webapp-python
---
-->

# Python web application - protected and accessing Microsoft Graph | Microsoft identity platform

<!-- Build badges here
![Build passing.](https://img.shields.io/badge/build-passing-brightgreen.svg) ![Code coverage.](https://img.shields.io/badge/coverage-100%25-brightgreen.svg) ![License.](https://img.shields.io/badge/license-MIT-green.svg)
-->

This sample demonstrates a Python Flask web application that is both protected by Microsoft identity platform and accesses Microsoft Graph as the user by using the Microsoft Authentication Library (MSAL) for Python..

![A browser screenshot on a page showing a response from Microsoft Graph](./app.png)

> :page_with_curl: This sample application backs one or more technical articles on docs.microsoft.com. <!-- TODO: Link to first tutorial in series when published. -->

## Prerequisites

- Python 3.8+

## Setup

### 1. Register the app

First, complete the steps in [Register an application with the Microsoft identity platform](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app) to register the sample app.

Use these settings in your app registration.

| App registration <br/> setting | Value for this sample app                                                  | Notes                                                                                              |
|:----------------------------:|:-----------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|
| **Name**                     | `python-webapp`                                                              | Suggested value for this sample. <br/> You can change the app name at any time.                    |
| **Supported account types**  | **Accounts in this organizational directory only (Single tenant)**           | Suggested value for this sample.                                                                   |
| **Platform type**            | **Web**                                                                      | Required value for this sample. <br/> Enables the required and optional settings for the app type. |
| **Redirect URI**             | `http://localhost:5000/auth/redirect`                                        | Required value for this sample.                                                                    |
| **Client secret**            | _Value shown in Azure portal_                                                | :warning: Record this value immediately! <br/> It's shown only _once_ (when you create it).        |
| **Implicit grant & hybrid flows** | _None selected_                                                         | This sample does not use the implicit grant or hybrid flows.                                       |
| **Allow public client flows** | **No**                                                                      | This sample does not use a public client flow.                                                     |
| **Token configuration**      | _No additional claims_                                                       | This sample does not rely on any additional claims existing in the tokens.                         |
| **App roles**                | _Add an App role called `admin` for use by **Users/Groups**_                 | Required value for this sample. <bn /> One route requires your user to be assigned this role.      |

> :information_source: **Bold text** in the table matches (or is similar to) a UI element in the Azure portal, while `code formatting` indicates a value you enter into a text box in the Azure portal.

Use these settings in your Enterprise Application for this sample app

| Enterprise Application <br/> setting | Value for this sample app                                            | Notes                                                                                              |
|:------------------------------------:|:---------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|
| **Users and groups**                 | _Add yourself with the **Role** of **admin**_                        | Required value for this sample. <bn /> One route requires your user to be assigned this role.      |

> :information_source: **Bold text** in the table matches (or is similar to) a UI element in the Azure portal, while `code formatting` indicates a value you enter into a text box in the Azure portal.

### 2. Update code sample with app registration values

Open the _default\_settings.py_ file and modify the three Azure Active Directory configuration properties using the values from your [app's registration in the Azure portal](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app).

- `CLIENT_ID`: `"Application (client) ID"`
- `AUTHORITY`: `"https://login.microsoftonline.com/{your tenant}"`
- `CLIENT_CREDENTIAL`: `"********"`

### 3. Install package(s)

To install Flask and msal into your (virtual) environment:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
flask run --host=localhost
```

## Browse to the application

Open your browser and navigate to **http://localhost:5000**. If everything worked, the sample app should produce output similar to this:

![A browser screenshot showing the weclome page to the sample application.](./app.png)

## About the code

This python web application is using the Flask web framework. It includes three navigatable routes with three different authentication/authorization levels required. As soon as the user navigates to a route that requires authentication, the user will be redirected to the Azure AD to sign in (if not already signed in via single sign-on) and accept the required app permissions.

Please be aware that all of the controller method processing is performed "inline" in the body of the controller. Meaning, the code does not rely on any Flask frameworks (or even utility methods) to ensure that the interplay between the Microsoft Authentication Library (MSAL) and the Flask session is understood. In practice you'd of course handle cross-cutting concerns such as authorization, authentication, session management in a more Flask-native way, reducing duplication and abstracting the logic away from the specific purpose of the controller method.

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