status_meaning ="""
| Status                | Local Uncommitted Changes | Local Commits Ahead | Local Commits Behind  |
|-----------------------|---------------------------|---------------------|-----------------------|
| `in_sync`             | FALSE                     | FALSE               | FALSE                 |
| `local_uncommitted`   | TRUE                      | None                | None                  |
| `local_behind`        | None                      | FALSE               | TRUE                  |
| `local_ahead`         | None                      | TRUE                | FALSE                 |
| `diverged`            | None                      | TRUE                | TRUE                  |
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from multiprocessing import Pool
from os import path, listdir
import subprocess
import pandas


def local_uncommitted(dir_path):
    """
    Return True if there is uncommitted local files.
    Return False if there is no uncommitted local files.
    """
    uncommited_command = "git status --porcelain | grep -q . && echo 'True'"
    response =  subprocess.run(uncommited_command, cwd=dir_path, shell=True, text=True, capture_output=True)
    
    return bool(response.stdout.strip())


def local_ahead_behind(dir_path):
    """
    Return integer between [0 , n] {n>0, n = number of commits ahead}
    """
    subprocess.run("git fetch", shell=True, cwd=dir_path, capture_output=True)
    local_ahead_command  = "git rev-list --count origin/main..HEAD"
    local_behind_command = "git rev-list --count HEAD..origin/main"
    count_ahead  = int(subprocess.run(local_ahead_command,  cwd=dir_path, shell=True, capture_output=True, text=True).stdout)
    count_behind = int(subprocess.run(local_behind_command, cwd=dir_path, shell=True, capture_output=True, text=True).stdout)
    return count_ahead, count_behind

def dir_git_status(dir_path, dir_name):
    data  = {"repo": dir_name}
    
    count_ahead, count_behind = local_ahead_behind(dir_path)
    is_uncommitted =  local_uncommitted(dir_path)

    status = []
    if not is_uncommitted and count_ahead == 0 and count_behind == 0:
        status.append("in_sync")
    if is_uncommitted:
        status.append("local_uncommited")
    if count_ahead == 0 and count_behind > 0:
        status.append("local_behind")
    if count_behind == 0 and count_ahead > 0:
        status.append("local_ahead")
    if count_ahead > 0 and count_behind > 0:
        status.append("diverged")
    
    data["local_uncommitted"] = is_uncommitted
    data["local_ahead"] = count_ahead > 0
    data["local_behind"] = count_behind > 0
    data["status"] = status
    
    return data

def report (root_dir, filter_dir=[], processes=None):
    report = []
    
    list_dir_name = listdir(root_dir)
    
    if filter_dir:
        list_dir_name = [dir_name for dir_name in list_dir_name if dir_name in filter_dir]

    if not processes:
        # Number of workers handling dir_git_status
        # I set it to 12 to match my fabulous 4core
        processes = 12 # Default

    with Pool(processes) as pool:
        # For parallel processing, we pass all dir_git_status() arguments to a pool. 
        # The pool runs in parallel : dir_git_status([(dir_1_path, dir_1_name), (dir_2_path, dir_2_name), ...])
        # Otherwise it takes forever to get a full report on more than 10 git repositories
        arguments = [(path.join(root_dir, dir_name), dir_name) for dir_name in list_dir_name] 
        report = pool.starmap(func=dir_git_status, iterable=arguments, )
    
    return pandas.DataFrame(report).to_markdown()

if __name__ == '__main__':
    parser = ArgumentParser(
        description= f"Git repository status report : {status_meaning}",
        formatter_class= RawDescriptionHelpFormatter
    )
    parser.add_argument("root_dir", 
                        help="The root_dir where the git repos are stored")
    
    parser.add_argument("--filter_dir", 
                        required=False,
                        metavar="DIRS",
                        help="""Filter report to specific directories --filer_dir "dir_1, ..., dir_n" """)

    parser.add_argument("--processes", 
                        required=False,
                        metavar="PRCS",
                        help="""Number of worker running the status check. Default 12 """)
    
    args = parser.parse_args()
    
    print(
        report(args.root_dir, args.filter_dir)
          )