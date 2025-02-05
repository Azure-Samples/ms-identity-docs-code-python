import os
import json

from django.conf import settings
from django.shortcuts import render
import requests


__version__ = "0.5.0"


@settings.AUTH.login_required
def index(request, *, context):
    return render(request, 'index.html', dict(
        user=context['user'],
        edit_profile_url=settings.AUTH.get_edit_profile_url(),
        api_endpoint=os.getenv("ENDPOINT"),
        title=f"Microsoft Entra ID Django Web App Sample v{__version__}",
    ))

@settings.AUTH.login_required(scopes=os.getenv("SCOPE", "").split())
def call_api(request, *, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render(request, 'display.html', {
        "title": "Result of API call",
        "content": json.dumps(api_result, indent=4),
    })

