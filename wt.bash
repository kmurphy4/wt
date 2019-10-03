#!/bin/bash
#
# Kevin Murphy
# 10/3/19
#
# https://github.com/keggsmurph21/wt
# wt entrypoint and bash completion function. source this file
# in your .bashrc or .bash_profile to use it

wt() {
    local path=/path/to/wt
    cd $(python3 $path/main.py $@)
}

__wt_complete() {
    # adapted from https://www.endpoint.com/blog/2016/06/03/adding-bash-completion-to-python-script
    local curr prev cmds wts opts
    COMPREPLY=()
    curr="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmds="list use"
    worktrees="$(git worktree list --porcelain 2>/dev/null \
        | awk 'NR % 4 == 3' \
        | sed -E 's,.*refs/heads/,,')"

    case "$prev" in
        wt)     opts="$cmds" ;;
        use)    opts="$worktrees" ;;
        list)   opts="" ;;
        *)      opts="" ;;
    esac

    COMPREPLY=( $(compgen -W "$opts" -- $curr) )
}

complete -F __wt_complete wt
