#!/bin/bash

PROJECT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"  
PROJECT=$(pwd | awk -F / '{print $NF}')

mkdir src
cd src

PRO_FILE=$PROJECT.pro

echo "create PRO file"
echo "TEMPLATE = app" > $PRO_FILE
echo "TARGET = $PROJECT" >> $PRO_FILE

echo "" >> $PRO_FILE
echo "QT += gui" >> $PRO_FILE 
echo "CONFIG += c++latest" >> $PRO_FILE

echo "" >> $PRO_FILE
echo "DESTDIR = \$\$PWD/../bin" >> $PRO_FILE

echo "" >> $PRO_FILE

cd ..

echo "create gitignore in $PROJECT"

echo "/bin" > .gitignore
echo "**/*.user" >> .gitignore
echo "**/build-*" >> .gitignore

cp $PROJECT_SCRIPT_DIR/_clang-format _clang-format

if [ -d .git ]
then
   git add .gitignore
   git add src/*
   git add src/_clang-format
   git commit -m "project infrastructure"
fi

