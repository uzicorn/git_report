# GIT STATUS REPORT

## Context
I have a lot of ongoing git projects, some of them are collaborations with other devs, some others are personal markdown notes i store on github, usually taken on my phone when i don't have my laptop. Last case is when i dev in an other machine.

## Goal 
- Dev a local script that runs inside my project code repository.
- Each sub-directory is a git repo. The script output must be a report on the versioning status between **local** and **remote**.
- Run parallel  

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

- `dir_[1::n]` are all **git repositories** linked to their remote branch. Locally, they are inside `$(root_dir)`
- You want a report on `dir_[1::n]` inside `$(root_dir)`
```bash
    pip install -r requirements.txt
    python3 path-to/git_report.py --help
    python3 path-to/git_report.py $(root_dir)
    python3 path-to/git_report.py $(root_dir) --filter_dir "dir_1, ... ,dir_n"
```
#### Outputs 
- You ran `py -m git_report.git_report $(root_dir)`
  
|    | repo                   | local_uncommitted   | local_ahead   | local_behind   | status      |
|---:|:-----------------------|:--------------------|:--------------|:---------------|:------------|
|  0 | dir_1                  | False               | False         | False          | ['in_sync'] |
|  1 | dir_2                  | True                | False         | False          | ['local_uncommitted'] |
|  2 | dir_3                  | False               | True          | False          | ['local_ahead'] |
|  3 | dir4                   | False               | False         | True           | ['local_behind'] |
|  4 | dir_5                  | False               | True          | True           | ['diverged'] |
|  5 | dir_6                  | True                | True          | False          | ['local_uncommitted', 'local_ahead'] |
|  6 | dir_7                  | True                | False         | True           | ['local_uncommitted', 'local_behind'] |
|  7 | dir_8                  | True                | True          | True           | ['local_uncommitted', 'diverged'] | 

- You ran `py -m git_report.git_report $(root_dir) --filter_dir "dir_1, dir_2, dir_3"` :

|    | repo                   | local_uncommitted   | local_ahead   | local_behind   | status      |
|---:|:-----------------------|:--------------------|:--------------|:---------------|:------------|
|  0 | dir_1                  | False               | False         | False          | ['in_sync'] |
|  1 | dir_2                  | True                | False         | False          | ['local_uncommitted'] |
|  2 | dir_3                  | False               | True          | False          | ['local_ahead'] |

## Git commands used in the script

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
