import msal
import webbrowser
import Managers.DirectoryManager as dm
from Managers.ErrorConfig import ErrorCodes

'''
Creates access token for Graph API if there is none.
    How it works:
        1. Run method GenerateAccessToken()
            1.1 If there is available it will just take that access token
        2. If not, a code will be generated in the terminal to be used to authenticate account
        3. Paste code and sign into the account allow access to calendars
'''
# 
# 
### 
###

APP_ID='99b8766f-5d52-490c-8237-187338d09615'

SCOPES = ['Calendars.Read', 
          'Calendars.Read.Shared', 
          'Calendars.ReadBasic', 
          'Calendars.ReadWrite', 
          'Calendars.ReadWrite.Shared']

def GenerateAccessToken():
    # graph_url = 'https://graph.microsoft.com/v1.0/'
    authority_url = 'https://login.microsoftonline.com/ffd89303-ce5f-4918-85cf-8f76dc05770e/'
    #authority_url = 'https://login.microsoftonline.com/consumers/'

    access_token_cache = msal.SerializableTokenCache()

    token_path = f'{dm.getCurrentFileDirectory(__file__)}/api_token_access.json'
    if dm.checkPathExists(token_path):
        access_token_cache.deserialize(open(token_path, 'r').read())

    client = msal.PublicClientApplication(client_id=APP_ID, 
                                          authority=authority_url,
                                          token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts: token_response = client.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        flow = client.initiate_device_flow(scopes=SCOPES)

        if 'user_code' not in flow:
            ErrorCodes.PrintCustomError(f"FAILED TO INITIATE DEVICE FLOW: {flow.get('error')}")
            exit()
        
        print(flow['user_code'])
        webbrowser.open(flow['verification_uri'])

        token_response = client.acquire_token_by_device_flow(flow=flow)

    with open(f'{token_path}', 'w') as file:
        file.write(access_token_cache.serialize())

    return token_response



