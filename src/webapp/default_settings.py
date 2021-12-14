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
# See README.md for more details
CLIENT_ID = ""
CLIENT_CREDENTIAL = ""
AUTHORITY = ""
