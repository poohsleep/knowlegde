Git Skills
===
Mac OSX
-----
```sh
$ brew update
--if uninitialized constant Formulary::HOMEBREW_CORE_FORMULA_REGEX
run it again
$ brew upgrade git
$ git --version
git version 2.5.1
```
Ubuntu
-----
Upgrade
>Add the Software Source for the Ubuntu Git Maintainers Team. To get the very latest version of git, you need to add the PPA (Personal Package Archive) from the Ubuntu Git Maintainers Team to your Software Source list. Do that with the add-apt-repository command to add the PPA:

    $ sudo add-apt-repository ppa:git-core/ppa
Then update the source list and upgrade git:

    $ sudo apt-get update
    $ sudo apt-get install git
    $ git --version
    git version 2.5.1
Commands
------
Revert to old commit and push it to head

    $git checkout master
    $git reset --hard 0d1d7fc32
    $git push -f origin master
    $git push -f heroku master
[Revert to old commit](
http://stackoverflow.com/questions/4114095/revert-to-a-previous-git-commit)

    $ git checkout -b old-state 0d1d7fc32
[Delete pushed ignore file](
http://stackoverflow.com/questions/1139762/ignore-files-that-have-already-been-committed-to-a-git-repository)
    git rm --cached "filename"
    git rm -r --ignore-unmatch  ./path/file
    git add .
    git commit -m "..."
    git push
Merge local branch to local branch and push local branch after merging (target branch: dev, local: prod)
    
    $ git checkout prod
    $ git merge dev
    $ git push origin prod
Merge remote branch to local branch and push local branch after merging (remote: dev, local: prod)

    $ git checkout prod
    $ git merge origin/dev
    $ git push origin prod
    
Save current workspace temporally, to see another branch. current branch <branchA>
    
    $ git stash --help (optional)
    $ git stash
    $ git stash list (optional)
    $ git checkout <another branch>
    ...
    $ git checkout branchA
    $ git stash pop
Pull remote branch to local

    $ git checkout master
    $ git pull
    $ git branch -a (optional, show local and remote branches)
    or
    $ git pull -a
    $ git checkout <newbranch>
Delete remote branch
    
    $ git branch -r (optional, show remote branch)
    $ git push --delete origin <branchname>
    $ git remote prune origin  (refresh remote branches, in case of showing remote branch after deleting it)
Delete local branch

    $ git branch (optional, show local branch)
    (delete the branch which has been merged to HEAD)
    $ git branch -d <branchname>
    or (delete no matter the branch merged or not)
    $ git branch -D <branchname>
Ignore current changes(recover it to the status of last pull)

    $ git checkout .
Change changed files to a specific version

    $ git checkout <commit num> file/to/restore
Checkout branch specifying commit step

    $ git checkout -f step-3  (step3)
Alias

    $ git config --global alias.cm 'commit -m'
    $ git config --global alias.co 'checkout'
    $ git config --global alias.st 'status'
Default push

    $git config --global push.default simple
