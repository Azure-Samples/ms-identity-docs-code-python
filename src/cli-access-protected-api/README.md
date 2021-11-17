# Access a protected API from a Python app | Microsoft identity platform

This sample will eventually show how a python console application can access a protected API, as its own identity, using the [Microsoft Autentication Library (MSAL) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python). This scenario supports usages such as cron jobs and also direct cli invocation.

## Prerequisites

- Python 3

## Run without installing

Install application runtime dependencies:

```bash
pip install -r dev-requirements.txt
```

Run the application:

```bash
python3 cli.py
```

## Or install and run locally

Build and install the `msal-py-cli` python module.

```bash
pip install .
```

Run the application:

```bash
msal-py-cli -t <your-domain>.onmicrosoft.com -c <your-app-client-id> -o <your-app-object-id> -s <a non-expired app secret>
```

Example of the above:

```bash
msal-py-cli -t contoso.onmicrosoft.com -c 714c4653-8063-4a37-83bb-334a7fcfa389 -o cf43d75e-675d-4f3b-9f5e-571fa0922262 -s aVp7Q~CQP_4oSkH~KGDRn.z3X920EipYokQBO
```

Uninstall the application:

```bash
pip uninstall msal-py-cli
```