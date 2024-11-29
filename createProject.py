#!/usr/bin/env python3


import os
import shutil
import subprocess
from wapy.curses import PredfinedColor, CursesApp, CursesWindow, KeyAction


class BannerWindow(CursesWindow):

   def __init__(self, keyMap):

      self._keyMap = keyMap

      bannerHeight = 1 + len(self._keyMap)
      super().__init__(0, -(bannerHeight + 1), -1, bannerHeight)

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

   class Feature:

      def __init__(self, enabled, description, cursorPos, category):

         self.enabled = enabled
         self.description = description
         self.cursorPos = cursorPos
         self.category = category

   def __init__(self, screen):

      keyMap = dict()
      keyMap[' '] = KeyAction(self.toggle, False, 'toggle')
      keyMap['c'] = KeyAction(self.create, True, 'create')
      keyMap['q'] = KeyAction(None, True, 'quit')

      super().__init__(screen, keyMap)

      self.bannerWindow = BannerWindow(keyMap)
      self.addWindow(self.bannerWindow)

      self.createWindow(0, 0, -1, 1, PredfinedColor.HEADER, self.fillHeader)
      self.createWindow(0, -1, -1, 1, PredfinedColor.HEADER, self.fillFooter)

      self.projectPath = os.getcwd()
      self.name = os.path.basename(self.projectPath)

      scriptDir = os.path.abspath(__file__)
      self.scriptDir = os.path.dirname(scriptDir)

      self.features = {'app_wrapper': Project.Feature(True, 'Mac and Windows app', [0, 0], 'Qt'),
                       'icon': Project.Feature(False, 'App icon', [0, 1], 'Qt'),
                       'gui': Project.Feature(False, 'Gui', [0, 2], 'Qt'),
                       'widget': Project.Feature(True, 'Widgets', [0, 3], 'Qt'),
                       'network': Project.Feature(False, 'Network', [0, 4], 'Qt'),
                       'pre_compile': Project.Feature(True, 'Pre compiled Header', [1, 0], 'C++'),
                       'git_create': Project.Feature(False, 'Create Git repository', [1, 1], 'Git')}

      self.maxCursorPos = [1, 4]

   def create(self):

      os.chdir(self.projectPath)

      shutil.copy(self.scriptDir + '/_clang-format', '_clang-format')
      with open('.gitignore', 'w') as gitignore:
         gitignore.write('/bin\n')
         gitignore.write('**/*.user\n')
         gitignore.write('**/build\n')

      self._createCmakeFile()
      self._doGitThings()

   def toggle(self):

      for _, feature in self.features.items():
         if self.cursorPos == feature.cursorPos:
            feature.enabled = not feature.enabled
            return

   def fillScreen(self, screen):

      lineOffset = 4

      screen.addstr(2, 1, 'Qt Features:')
      line = 0
      for _, feature in self.features.items():
         if feature.category != 'Qt':
            continue
         self.addCheckBox(line + lineOffset, 1, feature.description, feature.enabled, self.cursorPos == feature.cursorPos)
         line += 1

      screen.addstr(2, 30, 'Other Features:')
      line = 0
      for _, feature in self.features.items():
         if feature.category == 'Qt':
            continue
         self.addCheckBox(line + lineOffset, 30, feature.description, feature.enabled, self.cursorPos == feature.cursorPos)
         line += 1

   def cursorUpdated(self):

      if self.cursorPos[0] == 1 and self.cursorPos[1] > 1:
         self.cursorPos[0] = 0

   def fillHeader(self, header):

      header.addstr(0, 1, 'Create CMAKE project for ')
      header.addstr(0, 26, self.name, PredfinedColor.HEADER_HIGHLIGHT)

   def fillFooter(self, footer):

      # footer.addstr(0, 1, f'{self.projectPath} @ [{self.cursorPos[0]}, {self.cursorPos[1]}]')
      footer.addstr(0, 1, f'{self.projectPath}')

   def _featureEnabled(self, key):

      if not key in self.features:
         return False

      return self.features[key].enabled

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

      gitAvaialbale = not os.path.exists('.git')

      if self._featureEnabled('git') and not gitAvaialbale:
         subprocess.run(['git', 'init'])
         gitAvaialbale = True

      if not gitAvaialbale:
         return

      subprocess.run(['git', 'add', '.gitignore'])
      subprocess.run(['git', 'add', '_clang-format'])
      subprocess.run(['git', 'add', 'CMakeLists.txt'])
      if os.path.exists(f'{self.name}.precompiled.h'):
         subprocess.run(['git', 'add', f'{self.name}.precompiled.h'])
      subprocess.run(['git_create', 'commit', '-m', '"first commit"'])


if __name__ == '__main__':

   Project.main()
