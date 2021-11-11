# Access a protected API from a Python app | Microsoft identity platform

This sample will eventually show how a python console application can access a protected API, as its own identity, using the [Microsoft Autentication Library (MSAL) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python). This scenario supports usages such as cron jobs and also direct cli invocation.

**This sample is still in early development.  Please do not use/reference at this time.**

## Prerequisites

- Python 3

## Run without installing

Install application runtime dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 cli.py
```

## Or install and run locally

Before you can build the application for installing in your system (or virtual environment), ensure you have `wheel` available in your environment

```bash
pip install wheel
```

Build and install the `docs-ms-identity-py-clientcredential` python module.

```bash
pip install .
```

Run the application:

```bash
docs-ms-identity-py-clientcredential
```

Uninstall the application:

```bash
pip uninstall docs-ms-identity-py-clientcredential
```