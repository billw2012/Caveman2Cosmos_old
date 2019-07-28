@echo off
PUSHD "%~dp0"
REM make sure we are on latest from svn in get svn branch
call _RebaseFromSVN.bat
REM update local git svn branch
cd /d C:\Users\billw\Documents\Github\Caveman2Cosmos 
git checkout svn 
git fetch origin 
git merge origin/svn 
REM update svn repository locally
cd /d C:\Users\billw\Documents\SVN\Caveman2Cosmos
svn switch https://svn.code.sf.net/p/caveman2cosmos/code/branches/billw-git
svn update
REM mirror git svn branch into svn repo
robocopy ..\..\GitHub\Caveman2Cosmos . /MIR /XD .git .svn
POPD