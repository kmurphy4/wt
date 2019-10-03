# wt

utility for wrapping around `git worktree`, allowing easy navigation between trees

### installation

```bash
$ git clone https://github.com/keggsmurph21/wt.git ~/.wt
$ cd ~/.wt
$ ./install
$ source ~/.bashrc
```

### usage

##### see current worktrees

```bash
$ wt list
worktrees:
  - master
  - feature-123
  - testing
  - stable
```

```bash
$ wt list --all
worktrees:
  - master                0123456 /path/to/master
  - feature-123           7890abc ~/.worktrees/:owner/:repo/feature-123
  - testing               1234567 ~/.worktrees/:owner/:repo/testing
  - stable                890abcd ~/.worktrees/:owner/:repo/stable
```

##### jump to a specific worktree

```bash
$ pwd
/path/to/master
$ wt use testing
$ pwd
~/.worktrees/:owner/:repo/testing
```

##### add a new worktree (coming soon)

```bash
$ pwd
/path/to/master
$ wt add new-branch # coming soon!
$ wt list
worktrees:
  - master
  - feature-123
  - testing
  - stable
  - new-branch
$ pwd
~/.worktrees/:owner/:repo/new-branch
```
