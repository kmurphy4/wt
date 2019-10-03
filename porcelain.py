import re
import subprocess

from WorktreeError import WorktreeError

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

def worktree_parse(text):
    match = re.match(r'^worktree (.*)\nHEAD ([0-9a-f]{40})\nbranch refs/heads/(.*)$', text)
    if match is None:
        raise WorktreeError(f'worktree-parse could not match text\n\n{text}')
    return match.group(1,2,3)

def get_current_branch():
    proc = run('git rev-parse --abbrev-ref HEAD')
    if proc.returncode > 0:
        raise WorktreeError(f'worktree-get-branch return code {proc.returncode}\n\n{proc.stderr}')
    return proc.stdout.strip()
