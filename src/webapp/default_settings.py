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

# 'Application (client) ID' of app registration in the Microsoft Entra admin center - this value is a GUID
CLIENT_ID = "Enter_the_Application_Id_Here"

# Client secret 'Value' (not its ID) from 'Client secrets' in app registration in the Microsoft Entra admin center
CLIENT_CREDENTIAL = "Enter_the_Client_Secret_Value_Here"

# 'Tenant ID' of your Microsoft Entra tenant - this value is a GUID
TENANT_ID = "Enter_the_Tenant_ID_Here"
