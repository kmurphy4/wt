import argparse
import os
import sys

from WorktreeError import WorktreeError
from Worktrees import Worktrees

def wt_use(cwd, args):
    trees = Worktrees(cwd)
    return trees.interpolate_path(args.branch, cwd)

def wt_list(cwd, args):
    trees = Worktrees(cwd)
    sys.stderr.write(trees.pretty_print(args.all) + '\n')
    return os.getcwd()

def wt_add(cwd, args):
    pass

if __name__ == '__main__':

    try: # protect against -euo pipefail, since this file is run in a sourced command

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='cmd')

        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-a', '--all', action='store_true')
        list_parser.set_defaults(func=wt_list)

        use_parser = subparsers.add_parser('use')
        use_parser.add_argument('branch')
        use_parser.set_defaults(func=wt_use)

        args = parser.parse_args()
        if args.cmd is None:
            raise WorktreeError('missing required arg: cmd')

        cwd = os.getcwd()
        dest = args.func(cwd, args)

        print(dest)

    except WorktreeError as e:
        sys.stderr.write(str(e) + '\n')
        print(os.getcwd())


