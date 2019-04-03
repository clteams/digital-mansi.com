#!/usr/bin/python3

import git

repo = git.Repo("../")

a_commit = None
b_commit = None
for e, commit in enumerate(repo.iter_commits()):
    if not e:
        a_commit = commit
    elif e == 1:
        b_commit = commit
    else:
        break


diff = repo.git.diff(a_commit, b_commit, name_only=True)
for element in diff.split():
    print(element)
