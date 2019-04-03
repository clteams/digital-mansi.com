#!/usr/bin/python3

import git
import os
from collections import namedtuple


class File2Process:
    def __init__(self, file_path):
        self.folder_properties = namedtuple("FProps", ["auto_sync", "restart"])
        self.file_path = file_path
        try:
            self.symb_folder, self.in_folder = self.file_path.split('/', 1)
        except ValueError:
            self.symb_folder = False

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
        self.git_file = GitFile(self.file_path)

        self.folder_methods["html_pages"] = self.update_html_pages

    def update_file_tree(self):
        if not self.symb_folder:
            return

        if self.symb_folder not in self.folder_methods:
            return

        self.folder_methods[self.symb_folder]()

    def on_folder(self, folder_name):
        def wrapper(fn):
            def wrapped(*args):
                self.folder_methods[folder_name] = fn

            return wrapped

        return wrapper

    def update_html_pages(self):
        if self.git_file.status == "delete":
            os.remove("/var/www/html/%s" % self.in_folder)
        elif self.git_file.status in ["modify", "add"]:
            with open("/var/www/html/%s" % self.in_folder, "wb") as of:
                of.write(self.git_file.file_content)
                of.close()


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
    File2Process(element).update_file_tree()
