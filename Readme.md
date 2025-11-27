# TEST GIT REPO

## Goal 
- To dev a local script that runs inside my project code repository.
- Each sub-directory is a git repo. The script output must be a report on the versioning status between **local** and **remote**.
``` bash
/home/uzicorn/code/is_git:
    ├── acopole
    ├── bank_account_analysis
    ├── books-memento
    ├── cvtheque
    ├── dispatcher
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
Each repo can have up to 2 statuses 
- in_sync
- local_uncommitted
- local_uncommitted + [local_behind, local_ahead, diverged]
- local_behind
- local_ahead
- diverged

## Git commands

