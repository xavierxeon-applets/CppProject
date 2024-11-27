#!/usr/bin/env python3

import curses
import os
import shutil
import subprocess
from wapy.curses import PredfinedColor, CursesApp, CursesWindow, KeyAction


class BannerWindow(CursesWindow):

   def __init__(self, keyMap):

      self._keyMap = keyMap

      bannerHeight = 1 + len(self._keyMap)
      height, width = CursesApp.screen.getmaxyx()
      super().__init__(bannerHeight, width, height - (bannerHeight + 1), 0)

      self.backgroundColor = PredfinedColor.BANNER

   def draw(self, window):

      window.addstr(0, 1, 'Keyboard usage:', PredfinedColor.BANNER_HIGHLIGHT)
      line = 1
      for key, action in self._keyMap.items():
         if ' ' == key:
            key = 'space'
         window.addstr(line, 1, f'* {action.helpText} ({key})')
         line += 1


class Project(CursesApp):

   def __init__(self, screen):

      keyMap = dict()
      keyMap[' '] = KeyAction(self.toggle, False, 'toggle')
      keyMap['c'] = KeyAction(self.create, True, 'create')
      keyMap['q'] = KeyAction(None, True, 'quit')

      super().__init__(screen, keyMap)

      self.bannerWindow = BannerWindow(keyMap)
      self.addWindow(self.bannerWindow)

      height, width = CursesApp.screen.getmaxyx()
      self.createWindow(1, width, 0, 0, PredfinedColor.HEADER, self.fillHeader)
      self.createWindow(1, width, height - 1, 0, PredfinedColor.HEADER, self.fillFooter)

      self.projectPath = os.getcwd()
      self.name = os.path.basename(self.projectPath)

      scriptDir = os.path.abspath(__file__)
      self.scriptDir = os.path.dirname(scriptDir)

      self.features = {'app_wrapper': [True, 'Mac and Windows app'],
                       'icon': [False, 'App icon'],
                       'pre_compile': [True, 'Pre compiled Header'],
                       'gui': [False, 'Gui'],
                       'widget': [True, 'Widgets'],
                       'network': [False, 'Network'],
                       'git': [True, 'Create Git repository']}
      self.maxCursorIndex = len(self.features)

   def create(self, _):

      os.chdir(self.projectPath)

      shutil.copy(self.scriptDir + '/_clang-format', '_clang-format')
      with open('.gitignore', 'w') as gitignore:
         gitignore.write('/bin\n')
         gitignore.write('**/*.user\n')
         gitignore.write('**/build\n')

      self._createCmakeFile()
      self._doGitThings()

   def toggle(self, index):

      keys = list(self.features.keys())
      key = keys[index]
      feature = self.features[key]
      feature[0] = not feature[0]

   def fillScreen(self, screen, index):

      screen.addstr(2, 1, 'Qt Features:')
      lineOffset = 4

      line = 0
      for _, feature in self.features.items():
         check = '[x]' if feature[0] else '[ ]'
         checkColor = PredfinedColor.SELECTED if index == line else 0
         screen.addstr(line + lineOffset, 1, check, checkColor)
         screen.addstr(line + lineOffset, 5, feature[1])
         line += 1

   def fillHeader(self, header):

      header.addstr(0, 1, 'Create CMAKE project for ')
      header.addstr(0, 26, self.name, PredfinedColor.HEADER_HIGHLIGHT)

   def fillFooter(self, footer):

      footer.addstr(0, 1, self.projectPath)

   def _featureEnabled(self, key):

      if not key in self.features:
         return False

      return self.features[key][0]

   def _createCmakeFile(self):

      with open('CMakeLists.txt', 'w') as cmakefile:
         cmakefile.write('cmake_minimum_required(VERSION 3.20)\n')
         cmakefile.write(f'project({self.name} LANGUAGES CXX)\n')
         cmakefile.write('\n')
         cmakefile.write('set(CMAKE_CXX_STANDARD 20)\n')
         cmakefile.write('set(CMAKE_CXX_STANDARD_REQUIRED ON)\n')
         cmakefile.write('set(CMAKE_COMPILE_WARNING_AS_ERROR ON)\n')
         cmakefile.write('\n')
         cmakefile.write('if(NOT CMAKE_BUILD_TYPE)\n')
         cmakefile.write('   set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)\n')
         cmakefile.write('endif()\n')
         cmakefile.write('message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")\n')

         cmakefile.write('\n')
         cmakefile.write('find_package(Qt6 REQUIRED COMPONENTS')
         if self._featureEnabled('gui'):
            cmakefile.write(' Gui Svg')
         elif self._featureEnabled('widget'):
            cmakefile.write(' Widgets Svg')
         else:
            cmakefile.write(' Core')
         if self._featureEnabled('network'):
            cmakefile.write(' Network')
         cmakefile.write(')\n')

         cmakefile.write('set(CMAKE_AUTOUIC ON)\n')
         cmakefile.write('set(CMAKE_AUTOMOC ON)\n')
         cmakefile.write('set(CMAKE_AUTORCC ON)\n')
         cmakefile.write('\n')

         cmakefile.write('include_directories(${CMAKE_CURRENT_SOURCE_DIR})\n')
         cmakefile.write('\n')
         cmakefile.write('file(GLOB_RECURSE SOURCE_FILES\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.h\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.ui\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.qrc\n')
         cmakefile.write(')\n')
         cmakefile.write('\n')
         cmakefile.write('# remove build dir\n')
         cmakefile.write('list(FILTER SOURCE_FILES EXCLUDE REGEX "${PROJECT_SOURCE_DIR}/build/.*")\n')
         cmakefile.write('\n')

         cmakefile.write('qt_add_executable(${PROJECT_NAME} ${SOURCE_FILES})\n')
         if self._featureEnabled('pre_compile'):
            cmakefile.write('target_precompile_headers(${PROJECT_NAME} PUBLIC ${PROJECT_NAME}.precompiled.h)\n')
            cmakefile.write('target_sources(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}.precompiled.h)\n')
            if not os.path.exists(f'{self.name}..precompiledh'):
               with open(f'{self.name}.precompiled.h', 'w') as pre_compiled_header:
                  pre_compiled_header.write('#pragma once\n')
                  pre_compiled_header.write('\n')
                  pre_compiled_header.write('#include <QDebug>\n')

         if self._featureEnabled('app_wrapper'):
            cmakefile.write('\n')
            cmakefile.write('set_target_properties(${PROJECT_NAME} PROPERTIES\n')
            cmakefile.write('   WIN32_EXECUTABLE TRUE\n')
            cmakefile.write('   MACOSX_BUNDLE TRUE\n')
            cmakefile.write(')\n')

         if self._featureEnabled('icon'):
            cmakefile.write('\n')
            cmakefile.write('if(APPLE)\n')
            cmakefile.write('   set(MACOSX_BUNDLE_ICON_FILE ${PROJECT_NAME}.icns)\n')
            cmakefile.write('   set(APP_ICON ${CMAKE_CURRENT_SOURCE_DIR}/Resources/${PROJECT_NAME}.icns)\n')
            cmakefile.write('   set_source_files_properties(${APP_ICON} PROPERTIES MACOSX_PACKAGE_LOCATION "Resources")\n')
            cmakefile.write('   target_sources(${PROJECT_NAME} PRIVATE ${APP_ICON})\n')
            cmakefile.write('endif()\n')

         cmakefile.write('\n')
         cmakefile.write('target_link_libraries(${PROJECT_NAME} PRIVATE')
         if self._featureEnabled('gui'):
            cmakefile.write(' Qt6::Gui Qt6::Svg')
         elif self._featureEnabled('widget'):
            cmakefile.write(' Qt6::Widgets Qt6::Svg')
         else:
            cmakefile.write(' Qt6::Core')
         if self._featureEnabled('network'):
            cmakefile.write(' Qt6::Network')
         cmakefile.write(')\n')

   def _doGitThings(self):

      if self._featureEnabled('git') and not os.path.exists('.git'):
         subprocess.run(['git', 'init'])

      subprocess.run(['git', 'add', '.gitignore'])
      subprocess.run(['git', 'add', '_clang-format'])
      subprocess.run(['git', 'add', 'CMakeLists.txt'])
      if os.path.exists(f'{self.name}.precompiled.h'):
         subprocess.run(['git', 'add', f'{self.name}.precompiled.h'])
      subprocess.run(['git', 'commit', '-m', '"first commit"'])


if __name__ == '__main__':

   Project.main()
