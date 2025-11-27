import subprocess
import os

source = "/home/uzicorn/code/is_git/test"
uncommited_command = "git status --porcelain | grep -q . && echo 'True'"
local_uncommitted = subprocess.run(uncommited_command, cwd=source, shell=True, text=True, capture_output=True).stdout

if local_uncommitted:
    print(local_uncommitted.strip())
else :
    print("False")

