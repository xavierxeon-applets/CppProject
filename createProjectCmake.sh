#!/bin/bash

PROJECT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"  
PROJECT=$(pwd | awk -F / '{print $NF}')

echo "create CMakeLists.txt file"

echo "cmake_minimum_required(VERSION 3.20)" > CMakeLists.txt
echo "project($PROJECT LANGUAGES CXX)" >> CMakeLists.txt
echo "" >> CMakeLists.txt
echo "set(CMAKE_CXX_STANDARD 20)" >> CMakeLists.txt
echo "set(CMAKE_CXX_STANDARD_REQUIRED ON)" >> CMakeLists.txt
echo "set(CMAKE_COMPILE_WARNING_AS_ERROR ON)" >> CMakeLists.txt
echo "" >> CMakeLists.txt
echo "if(NOT CMAKE_BUILD_TYPE)" >> CMakeLists.txt
echo "   set(CMAKE_BUILD_TYPE Release CACHE STRING \"\" FORCE)" >> CMakeLists.txt
echo "endif()" >> CMakeLists.txt
echo "" >> CMakeLists.txt
echo "message(STATUS \"CMAKE_BUILD_TYPE: \${CMAKE_BUILD_TYPE}\")" >> CMakeLists.txt
echo "" >> CMakeLists.txt
#
echo "find_package(Qt6 REQUIRED COMPONENTS Widgets Svg)" >> CMakeLists.txt
echo "set(CMAKE_AUTOUIC ON)" >> CMakeLists.txt
echo "set(CMAKE_AUTOMOC ON)" >> CMakeLists.txt
echo "set(CMAKE_AUTORCC ON)" >> CMakeLists.txt
echo "" >> CMakeLists.txt

echo "include_directories(\${CMAKE_CURRENT_SOURCE_DIR})" >> CMakeLists.txt
echo "" >> CMakeLists.txt

echo "file(GLOB_RECURSE SOURCE_FILES" >> CMakeLists.txt
echo "   \${CMAKE_CURRENT_SOURCE_DIR}/*.h" >> CMakeLists.txt
echo "   \${CMAKE_CURRENT_SOURCE_DIR}/*.cpp" >> CMakeLists.txt
echo "   \${CMAKE_CURRENT_SOURCE_DIR}/*.hpp" >> CMakeLists.txt
echo "   \${CMAKE_CURRENT_SOURCE_DIR}/*.ui" >> CMakeLists.txt
echo "   \${CMAKE_CURRENT_SOURCE_DIR}/*.qrc" >> CMakeLists.txt
echo ")" >> CMakeLists.txt
echo "" >> CMakeLists.txt
echo "# remove build dir" >> CMakeLists.txt
echo "list(FILTER SOURCE_FILES EXCLUDE REGEX \"\${PROJECT_SOURCE_DIR}/build/.*\")" >> CMakeLists.txt
echo "" >> CMakeLists.txt

echo "qt_add_executable(\${PROJECT_NAME} \${SOURCE_FILES})" >> CMakeLists.txt
echo "" >> CMakeLists.txt
echo "target_link_libraries(\${PROJECT_NAME} PRIVATE Qt6::Widgets Qt6::Svg)" >> CMakeLists.txt
echo "" >> CMakeLists.txt

echo "create gitignore in $PROJECT"

echo "/bin" > .gitignore
echo "**/*.user" >> .gitignore
echo "**/build-*" >> .gitignore

cp $PROJECT_SCRIPT_DIR/_clang-format _clang-format

if [ -d .git ]
then
   git add .gitignore
   git add _clang-format
   git add CMakeLists.txt
   git commit -m "project infrastructure"
fi

