import requests
from flask import Flask, redirect, request, session
import uuid
import webbrowser
import threading
import os
import Managers.DirectoryManager as dir_manager

app = Flask(__name__)
app.secret_key = 'EventCalendarBuilder'  # Change this
local_host = 8000

CLIENT_ID = "99b8766f-5d52-490c-8237-187338d09615"
CLIENT_SECRET = "_xm8Q~VKXbbgvNF8mT5BUAMr5I_XyE3Q18aRNczT"
REDIRECT_URI=f'http://localhost:{local_host}/callback'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
SCOPES = "openid User.Read Calendars.ReadWrite"

@app.route('/')
def login():
    # Generate the full authorization endpoint on Microsoft's identity platform
    authorization_url = f"{AUTHORITY_URL}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&response_mode=query&scope={SCOPES}&state={uuid.uuid4()}"

    # Open the browser for authentication
    webbrowser.open(authorization_url)

    return "Authentication started. Please check your browser."

@app.route('/callback')
def callback():
    print(session['token'])
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
    token = token_r.json().get("access_token")
    session['token'] = token  # Store the token in the session
    return redirect('/create_event')

@app.route('/create_event')
def create_event():
    token = session.get('token')
    if not token:
        return "Not authenticated."
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Sample data for creating an event
    event_data = {
        "subject": "Test Event",
        "start": {
            "dateTime": "2023-11-01T12:00:00",
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": "2023-11-01T13:00:00",
            "timeZone": "UTC"
        },
        "body": {
            "contentType": "HTML",
            "content": "Event details here"
        }
    }

    response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event_data)
    return str(response.json())

def start():
    # Only run open_browser in the main Werkzeug process
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=login).start()
    app.run(host='localhost', debug=True, port=local_host)