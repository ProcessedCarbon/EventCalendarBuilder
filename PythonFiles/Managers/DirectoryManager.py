from pathlib import Path
import os
import glob
from Managers.ErrorConfig import ErrorCodes
import json

def MakeDirectory(dir_path:Path, dir_name:str):
    try:
        _dir = Path(os.path.join(dir_path, dir_name))
        _dir.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        ErrorCodes.PrintCustomError(e)

def WriteFile(dir_path:Path, file_name:str, content, write_type:['w', 'wb']='w')->bool:
    try:
        with open(Path(os.path.join(dir_path, file_name)), write_type) as file:
            file.write(content)
        file.close()
        return True
    except Exception as e:
        ErrorCodes.PrintCustomError(e)
        print(f'FAILED TO WRITE {file_name} TO {dir_path}')
        return False

def ReadFile(dir_path:Path, file_name:str, read_type:['r', 'rb']='r'):
    try:
        with open(Path(os.path.join(dir_path, file_name)), read_type) as file:
            content = file.read()
        file.close()
        return content
    except Exception as e:
        ErrorCodes.PrintCustomError(e)
        print(f'FAILED TO READ {file_name} TO {dir_path}')
        return False
    
def DeleteICSFilesInDir(dir_path:Path, file_type='ics')->bool:
    try:
        files = glob.glob(f"{dir_path}/*.{file_type}")
        for f in files:
            os.unlink(f)
        print(f'DELETE ALL FILES IN {dir_path} SUCCESSFULLY!')
        return True
    except:
        print(f'FAILED TO DELETE FILES IN {dir_path}')
        return False

def WriteJSON(dir_path:Path, file_name:str, content)->bool:
    try:
        with open(Path(os.path.join(dir_path, file_name))) as file:
            json.dump(content, file)
        return True
    except Exception as e:
        ErrorCodes.PrintCustomError("FAILED TO JSON DUMP:" + str(e))
        return False

def ReadJSON(dir_path:Path, file_name:str):
    file = os.path.join(dir_path, file_name)
    data = None

     # Check if file exists
    if os.path.getsize(file) == 0:
        ErrorCodes.PrintCustomError("FILE SIZE == 0")
        return None
    
    with open(file, 'r') as file:
        content = (file.read()).strip()  # Removes leading/trailing whitespaces

        # Return if file content is empty
        if not content:
            ErrorCodes.PrintCustomError("JSON IS EMPTY!")
            file.close()
            return None
        try:
            data = json.loads(content)

            # Check if file has valid json structure
            if not data:
                ErrorCodes.PrintCustomError("JSON FILE IS HAS EMPTY JSON STRUCT!")
                data = None
                file.close()
                return None
        except json.JSONDecodeError as e:
            # No need to set scheduled_data = None here as any changes made by try block wont persist if it fails
            ErrorCodes.PrintCustomError("INVALID JSON :" + str(e))
            return None
        
    file.close()
    return data


def getFilePath(dir_path:Path, file_name:str)->Path:
    return Path(os.path.join(dir_path, file_name))

def getAllFilePathsInDirectory(dir_path:Path, file_type='ics'):
        paths = glob.glob(f'{dir_path}/*.{file_type}')
        return paths
