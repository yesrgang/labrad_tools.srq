@echo off
:: suppress printing the executed commands to console

echo Running %~dp0%git_backup.bat ...
echo:
cd %~dp0

echo git status
git status --porcelain | findstr . && (set changes=1) || (set changes=0)
echo:

if %changes%==1 (
    echo commit all staged changes and push branch master to backup!

    git add --all
    git commit -m "Automatic backup commit"
    git push -u backup master
) else (
    echo no staged changes - nothing to commit/backup!
)

@echo on
