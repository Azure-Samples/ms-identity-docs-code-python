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

# 'Application (client) ID' of app registration in Azure portal - this value is a GUID
CLIENT_ID = ""

# Client secret 'Value' (not its ID) from 'Client secrets' in app registration in Azure portal
CLIENT_CREDENTIAL = ""

# Full directory URL, in the form of https://login.microsoftonline.com/<tenant>
AUTHORITY = ""
