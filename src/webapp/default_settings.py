# -*- coding: utf-8 -*-

"""
Flask environment configuration
"""

from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = True

# For local development purposes
SESSION_TYPE = "filesystem"

# Azure AD configuration - Update these three to your values

# This application's "Application (client) ID" found in this application's
# app registration in Azure Active Directory
# Example: "8a193f2d-e89d-c577-81b7-145f76344a77"
CLIENT_ID = ""

# Any of the non-expired "Client secrets" values found in this application's
# app registration in Azure Active Directory
# Example: "jPk7Q~NeKvlrrCj2_0tl~q-PR~o9Tp10W88"
CLIENT_CREDENTIAL = ""

# The tenant's "Primary domain" in which this application was registered,
# prefixed with https://login.microsoftonline.com/
# Example: "https://login.microsoftonline.com/contoso.onmicrosoft.com"
AUTHORITY = ""
