#!/bin/sh

#DATE=`date +%Y-%m-%d" "%H:%M`
DATE=`date +%YY%mm%dd`
MSG="$DATE"
if [ $# -gt 0 ]; then
    MSG="$1"
fi

#git checkout master

git diff --numstat origin/master

git add --all
git commit -am "${MSG}"

git push origin master