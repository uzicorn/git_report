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

print(f"local_uncommitted : {local_uncommitted(source)}")

def local_ahead(source):
    """
    Return integer between 0 and n (n>0, n = number of commits ahead) 
    """
    local_ahead_command = "git rev-list --count @{u}..HEAD"
    response = subprocess.run(local_ahead_command, cwd=source, shell=True, capture_output=True, text=True).stdout

    if response == "0":
        return False
    else:
        return (True, int(response))

print(f"local_ahead : {local_ahead(source)}")
    
