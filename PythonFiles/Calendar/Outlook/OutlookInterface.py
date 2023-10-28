import requests
from flask import Flask, request, jsonify
import uuid
import webbrowser
import threading
from Calendar.CalendarInterface import CalendarInterface
import Managers.DirectoryManager as directory_manager
import Managers.MultiprocessingManager as multiprocessing_mgr

app = Flask(__name__)
app.secret_key = 'EventCalendarBuilder'  # Change this
local_host = 8000

CLIENT_ID = "99b8766f-5d52-490c-8237-187338d09615"
CLIENT_SECRET = "_xm8Q~VKXbbgvNF8mT5BUAMr5I_XyE3Q18aRNczT"
REDIRECT_URI=f'http://localhost:{local_host}/callback'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "openid User.Read Calendars.ReadWrite"

token_path = directory_manager.getCurrentFileDirectory(__file__)

# Format:
# https://learn.microsoft.com/en-us/graph/api/calendar-post-events?view=graph-rest-1.0&tabs=http
class OutlookEvent():
    def __init__(self, 
                 name:str, location:str,  dtstart:str, 
                 dtend:str, tzstart:str, tzend:str, isonline=False) -> None:
        
        self.name = name
        self.location = location
        self.dtstart = dtstart
        self.dtend = dtend
        self.tzstart = tzstart
        self.tzend = tzend
        self.isonline = isonline
        
        self.event = {
            "subject": name,
            "body": {
                "contentType": "HTML",
                "content": ""
            },
            "start": {
                "dateTime": dtstart,
                "timeZone": tzstart
            },
            "end": {
                "dateTime": dtend,
                "timeZone": tzend
            },
            "location":{
                "displayName":location
            },
            "isOnlineMeeting": isonline,
            # "attendees": [
            #     {
            #     "emailAddress": {
            #         "address":"adelev@contoso.onmicrosoft.com",
            #         "name": "Adele Vance"
            #     },
            #     "type": "required"
            #     }
            # ],
            # "transactionId":"7E163156-7762-4BEB-A1C6-729EA81755A7"
            }
    
    def get_name(self):
        return self.name
    
    def get_location(self):
        return self.location
    
    def get_dtstart(self):
        return self.dtstart
    
    def get_dtend(self):
        return self.dtend
    
    def get_tzstart(self):
        return self.tzstart
    
    def get_tzend(self):
        return self.tzend
    
    def get_isonline(self):
        return self.isonline
    
@app.route('/')
def login():
    # Generate the full authorization endpoint on Microsoft's identity platform
    authorization_url = f"{AUTHORITY_URL}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope={SCOPES}&state={uuid.uuid4()}"

    # Open the browser for authentication
    webbrowser.open(authorization_url)

    return "Authentication started. Please check your browser."

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided."

    token_url = f"{AUTHORITY_URL}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    token_r = requests.post(token_url, data=token_data)
    directory_manager.WriteJSON(token_path, 'api_token_access.json', token_r.json())
    # multiprocessing_mgr.process_events['outlook_auth_event'].set()
    return 'Authentication Successful can close browser'

@app.route('/create_event')
def create_event():   
    token_access = directory_manager.ReadJSON(token_path, 'api_token_access.json')
    token = token_access['access_token']

    if not token:
        return jsonify(status="error", message="Not authenticated!"), 401
    
    event = request.json
    print(f'Request Args: \n {event} \n')

    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event['event'])
    return jsonify(status="success", message=f"Event created with status code: {response.status_code}")

# Only expecting 1 event per .ics file
def parse_ics(ics)->OutlookEvent:
    ics_file = CalendarInterface.ReadICSFile(ics)
    for component in ics_file.walk():
        if component.name == "VEVENT":
           return OutlookEvent(name=component.get('name'),
                                location=component.get("location"),
                                dtstart=component.get('dtstart').dt.isoformat(),
                                dtend=component.get('dtend').dt.isoformat(),
                                tzstart=str(component.get('dtstart').dt.tzinfo),
                                tzend=str(component.get('dtstart').dt.tzinfo)
                            )
    return None

def send_flask_req(req, json_data={})->bool:
    response = requests.get(f"http://localhost:{local_host}/{req}", json=json_data)
    print(f'Request completed with response {response.text} with status code {response.status_code}')
    '''
    HTTP status codes in the 200-299 range indicate success, with 200 being the standard response for a successful HTTP request.

    HTTP status codes in the 400-499 range indicate client errors. For instance, a 404 status code means "Not Found", and a 400 means "Bad Request".

    HTTP status codes in the 500-599 range indicate server errors.
    '''
    return 200 <= response.status_code < 300

def run():
    threading.Thread(target=login).start()
    app.run(host='localhost', port=local_host, use_reloader = False)