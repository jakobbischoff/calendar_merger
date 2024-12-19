import os
from datetime import datetime
import datetime

import msal
import requests

key_mapping = {
    'name': 'subject',
    'start': 'start',
    'end': 'end',
    'webLink': 'webLink',
    'all_day': 'isAllDay',
 }


def getMicrosoftEvents():
    scope = ['https://graph.microsoft.com/.default']
    tenant_id = os.environ['MICROSOFTTENANTID']
    client_id = os.environ['MICROSOFTCLIENTID']
    user_id = os.environ['MICROSOFTUSERID']
    client_secret = os.environ['MICROSOFTCLIENTSECRET']
    authority = 'https://login.microsoftonline.com/'+str(tenant_id)

    client = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )
    access_token = None
    token_result = client.acquire_token_silent(scope, account=None)
    if token_result:
        access_token = 'Bearer ' + token_result['access_token']

    # If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
    if not token_result:
        token_result = client.acquire_token_for_client(scopes=scope)
        access_token = 'Bearer ' + token_result['access_token']

    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/events?$filter=start/dateTime ge '2024-12-07T00:00:00Z'"

    headers = {
        'Authorization': access_token
    }

    # Make a GET request to the provided url, passing the access token in a header
    graph_result = requests.get(url=url, headers=headers)
    transformed_list = [
        {key: event.get(value, None) for key, value in key_mapping.items()}
        for event in graph_result.json()['value']
    ]
    for event in transformed_list:
        start_str = event['start']['dateTime']
        end_str = event['end']['dateTime']

        start = datetime.datetime.fromisoformat(start_str)
        end = datetime.datetime.fromisoformat(end_str)
        if event['all_day']:
            start = start.date()
            end = end.date()

        event['start'] = start
        event['end'] = end

    return transformed_list