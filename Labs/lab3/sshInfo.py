import json
import os

def sshInfo(file):

    if os.path.exists(file):
        with open(file,'r') as f:
            data = json.load(f)
            return data
    else:
        return False

