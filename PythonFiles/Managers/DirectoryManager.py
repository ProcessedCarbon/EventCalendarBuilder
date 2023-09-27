import os
from pathlib import Path

class DirectoryManager:    
    os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.absolute())
