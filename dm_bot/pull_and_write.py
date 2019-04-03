#!/usr/bin/python3

import git
from collections import namedtuple


class File2Process:
    def __init__(self, file_path):
        self.folder_properties = namedtuple("FProps", ["auto_sync", "restart"])
        self.file_path = file_path
        self.symb_folder, self.in_folder = self.file_path.split('/', 1)

        self.symb_folders = {
            "html_pages": self.folder_properties(auto_sync=True, restart=False),
            "media_files": self.folder_properties(auto_sync=True, restart=False),
            "publications": self.folder_properties(auto_sync=True, restart=False),
            "corpus_data": self.folder_properties(auto_sync=False, restart=False),
            "corpus_config": self.folder_properties(auto_sync=True, restart=True),
            "web_src": self.folder_properties(auto_sync=True, restart=False),
            "macros": self.folder_properties(auto_sync=True, restart=False),
            "dm_bot": self.folder_properties(auto_sync=False, restart=False),
        }

        self.folder_methods = dict()

    def on_folder(self, folder_name):
        def wrapper(fn):
            def wrapped(*args):
                self.folder_methods[folder_name] = fn

            return wrapped

        return wrapper


class GitFile:
    def __init__(self, file_path):
        global a_commit, b_commit
        global repo
        self.status = None
        self.file_content = None
        try:
            self.file_content = repo.commit(a_commit).tree[file_path].data_stream.read()
            try:
                fl = repo.commit(b_commit).tree[file_path].data_stream.read()
                self.status = "modify"
            except KeyError:
                self.status = "add"
        except KeyError:
            self.status = "delete"


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
