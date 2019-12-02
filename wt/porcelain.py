import os
import re
import subprocess

from .WorktreeError import WorktreeError

def run(command):
    return subprocess.run(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8')

def worktree_list():

    proc = run('git worktree list --porcelain')
    if proc.returncode > 0:
        raise WorktreeError(f'worktree-list returned code {proc.returncode}\n\n{proc.stderr}')

    worktrees = proc.stdout.strip().split('\n\n')
    return map(worktree_parse, worktrees)

def worktree_add(path, branch):

    proc = run(f'git worktree add {path} {branch}')
    if proc.returncode > 0:
        raise WorktreeError(f'worktree-add returned code {proc.returncode}\n\n{proc.stderr}')

    match = re.match(r'^HEAD is now at ([0-9a-f]+).*$', proc.stdout.strip())
    if match is not None:
        return path, match.group(1), branch

    raise WorktreeError(f'worktree-add could not match text \n\n{proc.stdout}')

def worktree_parse(text):
    match = re.match(r'^worktree (.*)\nHEAD ([0-9a-f]{40})\nbranch refs/heads/(.*)$', text)
    if match is not None:
        return match.group(1,2,3)
    raise WorktreeError(f'worktree-parse could not match text\n\n{text}')

def get_current_branch():
    proc = run('git rev-parse --abbrev-ref HEAD')
    if proc.returncode > 0:
        raise WorktreeError(f'worktree-get-branch returned code {proc.returncode}\n\n{proc.stderr}')
    return proc.stdout.strip()

def get_owner_and_repo():

    # first, make a guess based on remote/origin fetch URL
    proc = run('git remote show origin')
    if proc.returncode == 0:
        fetch_url = proc.stdout.split('\n')[1]
        match = re.match('.*?[:/]([-\w]+)/([-\w/]+)(.git)?', fetch_url)
        if match is not None:
            return match.group(1,2)

    # if that fails, guess repo based on path and unknown owner
    return 'unknown', os.path.basename(os.getcwd())
