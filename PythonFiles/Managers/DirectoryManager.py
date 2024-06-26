from pathlib import Path
import os
import glob
import json
import logging
import email

# No need to close file after 'with open()' is used
# Auto closes after with code is exceuted
def MakeDirectory(dir_path:Path):
    try:
        dir_path.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        logging.error(f'[{__name__}]: {e}')

def WriteFile(dir_path:Path, file_name:str, content, write_type:['w', 'wb']='w')->bool:
    try:
        with open(Path(os.path.join(dir_path, file_name)), write_type) as file:
            file.write(content)
        return True
    except Exception as e:
        logging.error(f'[{__name__}]FAILED TO WRITE {file_name} TO {dir_path} due to {e}')
        return False

def ReadFile(dir_path:Path, file_name:str, read_type:['r', 'rb']='r'):
    try:
        return FileRead(Path(os.path.join(dir_path, file_name)), read_type)
    except Exception as e:
        logging.error(f'[{__name__}] FAILED TO READ {file_name} TO {dir_path}')
        return False
    
def DeleteFilesInDir(dir_path:Path, file_type='ics')->bool:
    try:
        files = glob.glob(f"{dir_path}/*.{file_type}")
        for f in files:
            DeleteFile(f)
        logging.info(f'DELETE ALL FILES IN {dir_path} SUCCESSFULLY!')
        return True
    except:
        logging.error(f'FAILED TO DELETE FILES IN {dir_path}')
        return False

def DeleteFile(path:Path):
    os.unlink(path)

def WriteJSON(dir_path:Path, file_name:str, content)->bool:
    try:
        if content == None: open(Path(os.path.join(dir_path, file_name)), 'w').close()
        else:
            with open(Path(os.path.join(dir_path, file_name)), 'w') as file:
                json.dump(content, file)
        return True
    except Exception as e:
        logging.error(f"[{__name__}] FAILED TO JSON DUMP:" + str(e))
        return False

def ReadJSON(dir_path:Path, file_name:str):
    file = os.path.join(dir_path, file_name)
    data = None

    # Check if file exists
    if os.path.getsize(file) == 0:
        logging.info(f"[{__name__}] FILE SIZE == 0")
        return None
    
    with open(file, 'r') as file:
        content = (file.read()).strip()  # Removes leading/trailing whitespaces

        # Return if file content is empty
        if not content:
            logging.warning(f"[{__name__}] JSON IS EMPTY!")
            file.close()
            return None
        try:
            data = json.loads(content)

            # Check if file has valid json structure
            if not data:
                logging.warning(f"[{__name__}] JSON FILE IS HAS EMPTY JSON STRUCT!")
                data = None
                file.close()
                return None
        except json.JSONDecodeError as e:
            # No need to set scheduled_data = None here as any changes made by try block wont persist if it fails
            logging.error(f"[{__name__}]INVALID JSON : {str(e)}")
            return None
    return data

def ReadEMLFile(eml_file_path):
    try:
        # Open the .eml file
        with open(eml_file_path, 'r') as eml_file:
            # Parse the email message
            msg = email.message_from_file(eml_file)
            
            # Get the subject
            subject = msg['Subject']
            
            # Get the sender
            sender = msg['From']
            
            # Get the recipients
            recipients = msg['To']
            
            # Get the date
            date = msg['Date']
            
            # Get the plain text part of the email
            content =""
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    content += part.get_payload()
            return content, subject, sender, recipients, date
    except Exception as e:
        logging.error(f"[{__name__}]FAILED TO READ EML FILE WITH {str(e)}")

def getFilePath(dir_path:Path, file_name:str)->Path:
    return Path(os.path.join(dir_path, file_name))

def getAllFilePathsInDirectory(dir_path:Path, file_type='ics'):
    paths = glob.glob(f'{dir_path}/*.{file_type}')
    return paths

def getCurrentFileDirectory(file):
    return Path(os.path.dirname(os.path.realpath(file))).absolute()

def checkPathExists(path:Path)->bool:
    return os.path.exists(path)

def FileRead(file_path, read_type:['r', 'rb']='r'):
    with open(file_path, read_type) as file:
        content = file.read()
    return content