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
        self.folder_methods["media_files"] = self.update_media_files
        self.folder_methods["web_src"] = self.update_web_src

    def update_file_tree(self):
        if not self.symb_folder:
            return

        if self.symb_folder not in self.folder_methods:
            return

        self.folder_methods[self.symb_folder]()

    def update_dir_default(self, dir_path):
        if self.git_file.status == "delete":
            os.remove(dir_path + "/%s" % self.in_folder)
        elif self.git_file.status in ["modify", "add"]:
            with open(dir_path + "/%s" % self.in_folder, "wb") as of:
                of.write(self.git_file.file_content)
                of.close()

    def update_html_pages(self):
        self.update_dir_default("/var/www/html")

    def update_media_files(self):
        self.update_dir_default("/var/www/html/media")

    def update_web_src(self):
        self.update_dir_default("/var/www/html/web_src")


class DMBotPipeline:
    def __init__(self, rep, commit_msg, git_files, branch="master"):
        self.repo = rep
        self.commit_msg = commit_msg
        self.branch = branch
        self.branch_exists = True
        try:
            self.repo.git.checkout(self.branch)
        except git.CommandError:
            self.branch_exists = False
            self.repo.git.checkout("-b", self.branch)
        self.git_files = git_files

    def add_file_object(self, git_file):
        self.git_files.append(git_file)

    def apply(self):
        self.change_file_tree()
        self.commit()
        patch_local_files()
        self.push()

    def change_file_tree(self):
        for file in self.git_files:
            if file.status == "delete":
                os.remove(file.file_path)
            elif file.status in ["modify", "add"]:
                with open(file.file_path, "wb") as of:
                    of.write(file.file_content)
                    of.close()

    def commit(self):
        self.repo.git.add(update=True)
        self.repo.index.commit(self.commit_msg)

    def push(self):
        origin = self.repo.remote(name="origin")
        origin.push()


class CommitMessage:
    def __init__(self, main_components, sub_components=None):
        self._main = main_components
        self._sub = sub_components if sub_components else {}

    def new_text(self, text_msg):
        ix = 0
        while ix in self._main:
            ix += 1

        return {ix: text_msg}

    @staticmethod
    def _issue(issue_int, fixes=False, closes=False):
        issue = "#%d" % issue_int
        if fixes:
            issue = "Fixes " + issue
        elif closes:
            issue = "Closes " + issue

        return dict(_issue=issue)

    @staticmethod
    def _macro(**kwargs):
        in_paren = [kwargs[k] for k in ("name", "commit")]

        return dict(_macro="(macro %s)" % ", ".join(in_paren))

    def ser_main(self):
        return " ".join(sorted(self._main, key=lambda key: str(key)))

    def ser_sub(self):
        return " ".join(sorted(self._sub, key=lambda key: str(key)))

    def merge(self):
        return self.ser_main() + ("\n%s" % self.ser_sub() if self._sub else "")


class GitFile:
    def __init__(self, file_path, status=None, content=None):
        self.file_path = file_path
        self.status = None if not status else status
        self.file_content = None if not content else content
        if not self.status:
            self.set_status()

    def set_status(self):
        global a_commit, b_commit
        global repo
        try:
            self.file_content = repo.commit(a_commit).tree[self.file_path].data_stream.read()
            try:
                fl = repo.commit(b_commit).tree[self.file_path].data_stream.read()
                self.status = "modify"
            except KeyError:
                self.status = "add"
        except KeyError:
            self.status = "delete"


REPO_PATH = ".."
repo = git.Repo(REPO_PATH + "/")

a_commit = None
b_commit = None


def patch_local_files():
    global repo, a_commit, b_commit
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


if __name__ == "__main__":
    patch_local_files()
