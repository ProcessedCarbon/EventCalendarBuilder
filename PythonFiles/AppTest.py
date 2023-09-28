import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

# Extracts text from plain text file 
def getTestingText(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.read()
    
    return lines

def main():    
    pass

if __name__ == "__main__":
    main()