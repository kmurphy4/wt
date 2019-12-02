import os

from . import porcelain
from .WorktreeError import WorktreeError

class Worktrees():
    def __init__(self, cwd):

        self.new_worktrees_dir = os.path.expanduser('~/.worktrees')
        self._worktrees = {}
        for path, head, branch in porcelain.worktree_list():
            self._worktrees[branch] = Worktree(path, head, branch)

    def add(self, branch):
        owner, repo = porcelain.get_owner_and_repo()
        worktree_path = os.path.join(self.new_worktrees_dir, owner, repo, branch)
        if not os.path.exists(worktree_path):
            os.makedirs(worktree_path, exist_ok=True)
        path, head, branch = porcelain.worktree_add(worktree_path, branch)
        self._worktrees[branch] = Worktree(path, head, branch)

    def has(self, branch):
        return branch in self._worktrees

    def get(self, branch):
        return self._worktrees.get(branch, None)

    def interpolate_path(self, new_branch, cwd):

        current_branch = porcelain.get_current_branch()
        if not self.has(current_branch):
            raise WorktreeError(f'unrecognized branch: {current_branch}')
        current_path = self.get(current_branch).path
        subpath = cwd[ len(current_path): ]

        if not self.has(new_branch):
            raise WorktreeError(f'unrecognized branch: {new_branch}')

        path = self.get(new_branch).path
        for d in subpath.split('/'):
            candidate = os.path.join(path, d)
            if os.path.isdir(candidate):
                path = candidate

        return path

    def pretty_print(self, show_all):
        lines = ['worktrees:']
        for wt in self._worktrees.values():
            lines.append(f'  - {wt.pretty_print(show_all)}')
        return '\n'.join(lines)

class Worktree():
    def __init__(self, path, head, branch):

        self.path = path
        self._path = path.replace(os.path.expanduser('~'), '~')
        self.head = head
        self.branch = branch

    def pretty_print(self, show_all):
        if show_all:
            return f'{self.branch:30}\t{self.head[:7]}\t{self._path}'
        else:
            return self.branch
