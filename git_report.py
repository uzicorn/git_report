import subprocess
import os

source = "/home/uzicorn/code/is_git/test"
data  = {"local_uncommitted": None, "local_ahead": None, "local_behind": None, "status": []}

def local_uncommitted(source):
    """
    Return True if there is uncommitted local files.
    Return False if there is no uncommitted local files.
    """
    uncommited_command = "git status --porcelain | grep -q . && echo 'True'"
    response =  subprocess.run(uncommited_command, cwd=source, shell=True, text=True, capture_output=True)
    
    return bool(response.stdout.strip())


def local_ahead_behind(source):
    """
    Return integer between [0 , n] {n>0, n = number of commits ahead}
    """
    subprocess.run("git fetch", shell=True, cwd=source)
    local_ahead_command  = "git rev-list --count origin/main..HEAD"
    local_behind_command = "git rev-list --count HEAD..origin/main"
    count_ahead  = int(subprocess.run(local_ahead_command,  cwd=source, shell=True, capture_output=True, text=True).stdout)
    count_behind = int(subprocess.run(local_behind_command, cwd=source, shell=True, capture_output=True, text=True).stdout)

    return count_ahead, count_behind

count_ahead, count_behind = local_ahead_behind(source)
is_uncommitted =  local_uncommitted(source)

data["local_uncommitted"] = is_uncommitted
data["local_ahead"] = count_ahead > 0
data["local_behind"] = count_behind > 0

if not is_uncommitted and count_ahead == 0 and count_behind == 0:
    data["status"].append("in_sync")

if is_uncommitted:
    data["status"].append("local_uncommited")

if count_ahead == 0 and count_behind > 0:
    data["status"].append("local_behind")

if count_behind == 0 and count_ahead > 0:
    data["status"].append("local_ahead")

if count_ahead > 0 and count_behind > 0:
    data["status"].append("diverged")



print(data)