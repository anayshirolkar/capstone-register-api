# Contributing Guidelines

## Branching Strategy: GitHub Flow
GitHub Flow is adopted as we have only one release line in our project.

- Only one long-lived branch – `main`, which should always contain working and tested code.
- **Commits to `main` are prohibited.** Work should take place on short-lived branches and be merged via Pull Request.
- Short-lived branches will be created from `main` and deleted after being merged.

### Naming scheme for branches
| Prefix      | Use for                      | Example                      |
|-------------|------------------------------|------------------------------|
| `feature/`  | New functionality            | `feature/attendance-list`    |
| `fix/`      | Bugs fixing                  | `fix/wage-validation`       |
| `refactor/` | Code cleanup, no new behavior| `refactor/error-handling`   |
| `test/`     | Testing                      | `test/negative-cases`       |

## Commit guidelines
1. **Only one topic per commit.** `git add -p` can be used to stage only related commits.
2. **Subject line:** under 80 chars length, imperative mode
   (example: "Add attendance list endpoint").
3. **Commit body:** After blank line, contains:
   - what is different from before;
   - why the change was made;
   - any potential caveats;
   
## Integrating changes
- Merge feature branches into `main` using Pull Request after code reviewing.
  Never rebase commits that have been pushed to branch which is shared.
- Resolve merge conflicts locally, re-run the Newman tests, then commit the resolution.