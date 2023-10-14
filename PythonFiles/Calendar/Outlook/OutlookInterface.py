from Calendar.Outlook.MS_Graph import GenerateAccessToken, GRAPH_ENDPOINT
import requests

APP_ID='99b8766f-5d52-490c-8237-187338d09615'

# SCOPES = ['Calendars.Read', 
#           'Calendars.Read.Shared', 
#           'Calendars.ReadBasic', 
#           'Calendars.ReadWrite', 
#           'Calendars.ReadWrite.Shared']
SCOPES = ['Calendars.ReadWrite',]

access_token = GenerateAccessToken(app_id=APP_ID, scopes=SCOPES)
headers = {
    'Authorization' : 'Bearer' + access_token['access_token']
}

def ConstructEventDetail(name, **details):
    request_body={
        'subject' : name
    }

    for key, val in details.items():
        request_body[key] = val
    return request_body

#print(GRAPH_ENDPOINT + f'/me/events')
response = requests.post(GRAPH_ENDPOINT + f'/me/events', 
                         headers=headers,
                         json=ConstructEventDetail('Test 1'))

if response.status_code == 202: print(response.json())
else: print(response.reason)