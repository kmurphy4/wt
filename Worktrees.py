import os
import porcelain

from WorktreeError import WorktreeError

class Worktrees():
    def __init__(self, cwd):

        self._worktrees = {}
        for path, head, branch in porcelain.worktree_list():
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
        self.head = head
        self.branch = branch

    def pretty_print(self, show_all):
        if show_all:
            return f'{self.branch:30}\t{self.head[:7]}\t{self.path}'
        else:
            return self.branch
