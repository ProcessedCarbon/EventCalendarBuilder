import requests
from flask import Flask, request, jsonify
from uuid import uuid4
import webbrowser
import threading
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

from Calendar.CalendarInterface import CalendarInterface
from Calendar.Outlook.OutlookEvent import OutlookEvent
import Managers.DirectoryManager as directory_manager

APP = Flask(__name__)
APP.secret_key = 'EventCalendarBuilder'  # Change this
LOCAL_HOST = 8000

CLIENT_ID = "99b8766f-5d52-490c-8237-187338d09615"
CLIENT_SECRET = "_xm8Q~VKXbbgvNF8mT5BUAMr5I_XyE3Q18aRNczT"
REDIRECT_URI=f'http://localhost:{LOCAL_HOST}/callback'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "openid User.Read Calendars.ReadWrite"

TOKEN_PATH = directory_manager.getCurrentFileDirectory(__file__)

@APP.route('/')
def login():
    # Generate the full authorization endpoint on Microsoft's identity platform
    authorization_url = f"{AUTHORITY_URL}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope={SCOPES}&state={uuid4()}"

    # Open the browser for authentication
    webbrowser.open(authorization_url)

    return "Authentication started. Please check your browser."

@APP.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        directory_manager.WriteJSON(TOKEN_PATH, 'api_token_access.json', '')
        return "Failed Authentication."

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
    directory_manager.WriteJSON(TOKEN_PATH, 'api_token_access.json', token_r.json())
    return 'Authentication Successful can close browser'

@APP.route('/create_event')
def create_event():   
    token_access = directory_manager.ReadJSON(TOKEN_PATH, 'api_token_access.json')
    token = token_access['access_token']

    if not token: return jsonify(status="error", message="Not authenticated!"), 401
    
    event = request.json['event']
    
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event)
    return response.json()

@APP.route('/delete_event')
def delete_event():   
    token_access = directory_manager.ReadJSON(TOKEN_PATH, 'api_token_access.json')
    token = token_access['access_token']

    if not token:
        return jsonify(status="error", message="Not authenticated!"), 401
    
    event_id = request.json['event_id']

    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }

    response = requests.delete(f"https://graph.microsoft.com/v1.0/me/events/{event_id}", headers=headers)
    logging.info(f'DELETE RESPONSE STATUS CODE: {response.status_code}')
    return {}

@APP.route('/get_events')
def get_events():   
    token_access = directory_manager.ReadJSON(TOKEN_PATH, 'api_token_access.json')
    token = token_access['access_token']

    if not token:
        return jsonify(status="error", message="Not authenticated!"), 401
    
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(f"https://graph.microsoft.com/v1.0/me/events", headers=headers)
    logging.info(f'GET EVENTS RESPONSE STATUS CODE: {response.status_code}')
    return response.json()

@APP.route('/get_mail_settings')
def get_mail_settings():
    token_access = directory_manager.ReadJSON(TOKEN_PATH, 'api_token_access.json')
    token = token_access['access_token']
    headers = {
        'Authorization': f'{token_access["token_type"]} {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/mailboxsettings', headers=headers)
    logging.info(f'GET MAIL-SETTINGS RESPONSE STATUS CODE: {response.status_code}')
    return response.json()

# Only expecting 1 event per .ics file
def parse_ics(ics)->OutlookEvent:
    ics_file = CalendarInterface.ReadICSFile(ics)
    for component in ics_file.walk():
        if component.name == "VEVENT":
            rule=component.get('rrule').to_ical().decode(errors="ignore") if component.get('rrule') is not None else ''
            s_dt = component.get('dtstart').dt
            e_dt = component.get('dtend').dt
            return OutlookEvent(name=component.get('name'),
                                location=component.get("location"),
                                dtstart=s_dt.isoformat(),
                                dtend=e_dt.isoformat(),
                                tzstart='UTC',
                                tzend='UTC',
                                rrule=rule,
                                description=component.get('description')
                                )
    return None

# Require this to go from Flask -> Outlook
# send_flask_req will always return true if any sort of response is received
def send_flask_req(req, json_data={}, param_data={})->[bool, dict]:
    response = requests.get(f"http://localhost:{LOCAL_HOST}/{req}", json=json_data, params=param_data)
    '''
    HTTP status codes in the 200-299 range indicate success, with 200 being the standard response for a successful HTTP request.

    HTTP status codes in the 400-499 range indicate client errors. For instance, a 404 status code means "Not Found", and a 400 means "Bad Request".

    HTTP status codes in the 500-599 range indicate server errors.
    '''
    if 200 <= response.status_code < 300: return True, response.json()
    else: return False, {}

def run():
    login()
    APP.wsgi_app = ProxyFix(APP.wsgi_app)
    APP.run(host='localhost', port=LOCAL_HOST, use_reloader = False)

def start_flask():
    logging.info('ESTABLISHING CONNECTION TO OUTLOOK API THROUGH FLASK')
    flask_thread = threading.Thread(target=run)
    flask_thread.start()