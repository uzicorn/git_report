# GIT STATUS REPORT

## Context
I have a lot of ongoing git projects, some of them are collaborations with other devs, some others are personal markdown notes i store on github, usually taken on my phone when i don't have my laptop. Last case is when i dev in an other machine.

## Goal 
- Dev a local script that runs inside my project code repository.
- Each sub-directory is a git repo. The script output must be a report on the versioning status between **local** and **remote**.

``` bash
root_dir:
├── project_1
├── project_2
├── project_2
└── (...)

```
## Covered use cases

| Status                | Local Uncommitted Changes | Local Commits Ahead | Local Commits Behind  |
|-----------------------|---------------------------|---------------------|-----------------------|
| `in_sync`             | FALSE                     | FALSE               | FALSE                 |
| `local_uncommitted`   | TRUE                      | None                | None                  | 
| `local_behind`        | None                      | FALSE               | TRUE                  |
| `local_ahead`         | None                      | TRUE                | FALSE                 |
| `diverged`            | None                      | TRUE                | TRUE                  |

## Possible statuses per repo 
Each repo can have 1 up to 2 statuses : 
- in_sync
- local_uncommitted
- local_uncommitted + [local_behind, local_ahead, diverged]
- local_behind
- local_ahead
- diverged

## Usage
```bash
    py -m git_report --help
    py -m git_report.git_report $(root_dir)
    py -m git_report.git_report $(root_dir) --filter_dir "dir_1, ... ,dir_n"
```

## Git commands

**local branch ahead or behind relative to local**
```bash
git rev-list --count origin/main..HEAD  # Count the branches ahead  of local 
                     HEAD..origin/main  # Count the branches behind of local 
```

**Uncommitted changes in local branch**
```bash
git status --porcelain | grep -q . && echo 'True' # Returns True if one+ file is changed
```

## Licence 
No licence