import subprocess
import os

source = "/home/uzicorn/code/is_git/test"

def local_uncommitted(source):
    """
    Return True if there is uncommitted local files.
    Return False if there is no uncommitted local files.
    """
    uncommited_command = "git status --porcelain | grep -q . && echo 'True'"
    response =  subprocess.run(uncommited_command, cwd=source, shell=True, text=True, capture_output=True).stdout
    if response.strip() == "True":
        return True
    else:
        return False

print(local_uncommitted(source))