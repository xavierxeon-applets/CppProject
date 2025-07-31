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
                       'pre_compiled': Project.Feature(True, 'Use pre compiled Header', [1, 0], 'C++'),
                       'main_create': Project.Feature(True, 'Create main file', [1, 1], 'C++'),
                       'git_create': Project.Feature(False, 'Create Git repository', [1, 2], 'Git')}

      self.maxCursorPos = [1, 4]

   def create(self):

      os.chdir(self.projectPath)

      shutil.copy(self.scriptDir + '/_clang-format', '_clang-format')
      with open('.gitignore', 'w') as gitignore:
         gitignore.write('/bin\n')
         gitignore.write('**/*.user\n')
         gitignore.write('**/build\n')

      self._createCmakeFile()
      self._createOtherFiles()
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

         if self._featureEnabled('icon') or self._featureEnabled('pre_compiled'):
            cmakefile.write('find_package(WaTools REQUIRED)\n')
            cmakefile.write('\n')

         cmakefile.write('include_directories(${CMAKE_CURRENT_SOURCE_DIR})\n')
         cmakefile.write('\n')
         cmakefile.write('file(GLOB SOURCE_FILES\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.h\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.ui\n')
         cmakefile.write('   ${CMAKE_CURRENT_SOURCE_DIR}/*.qrc\n')
         cmakefile.write(')\n')
         cmakefile.write('\n')

         cmakefile.write('add_all_subdirs_files(${CMAKE_CURRENT_SOURCE_DIR})\n')
         cmakefile.write('\n')

         cmakefile.write('qt_add_executable(${PROJECT_NAME} ${SOURCE_FILES})\n')

         if self._featureEnabled('pre_compiled'):
            cmakefile.write('use_precompiled_headers()\n')
            cmakefile.write('\n')

         if self._featureEnabled('app_wrapper') and not self._featureEnabled('icon'):
            cmakefile.write('set_application_no_icon()\n')
            cmakefile.write('\n')

         if self._featureEnabled('icon'):
            cmakefile.write('set_application_icon(${CMAKE_CURRENT_SOURCE_DIR}/Resources/${PROJECT_NAME})\n')
            cmakefile.write('\n')

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

   def _createOtherFiles(self):

      if self._featureEnabled('main_create'):
         if self._featureEnabled('app_wrapper'):

            if not os.path.exists('MainWindow.h'):
               with open('MainWindow.h', 'w') as main_header:
                  main_header.write('#ifndef MainWindowH\n')
                  main_header.write('#define MainWindowH\n')
                  main_header.write('\n')
                  main_header.write('#include <QWidget>\n')
                  main_header.write('\n')
                  main_header.write('class MainWindow : public QWidget\n')
                  main_header.write('{\n')
                  main_header.write('   Q_OBJECT\n')
                  main_header.write('public:\n')
                  main_header.write('   MainWindow();\n')
                  main_header.write('};\n')
                  main_header.write('\n')
                  main_header.write('  # endif // NOT MainWindowH\n')
                  main_header.write('\n')

            if not os.path.exists('MainWindow.cpp'):
               with open('MainWindow.cpp', 'w') as main_source:
                  main_source.write('#include "MainWindow.h"\n')
                  main_source.write('\n')
                  main_source.write('#include <QApplication>\n')
                  main_source.write('\n')
                  main_source.write('MainWindow::MainWindow()\n')
                  main_source.write('   : QWidget(nullptr)\n')
                  main_source.write('{\n')
                  main_source.write('}\n')
                  main_source.write('\n')
                  main_source.write('// main function\n')
                  main_source.write('\n')
                  main_source.write('int main(int argc, char** argv)\n')
                  main_source.write('{\n')
                  main_source.write('   QApplication app(argc, argv);\n')
                  main_source.write('\n')
                  main_source.write('   MainWindow mw;\n')
                  main_source.write('   mw.show();\n')
                  main_source.write('\n')
                  main_source.write('   return app.exec();\n')
                  main_source.write('}\n')
                  main_source.write('\n')
         else:
            if not os.path.exists('main.cpp'):
               with open('main.cpp', 'w') as main_file:
                  main_file.write('#include <QApplication>\n')
                  main_file.write('\n')
                  main_file.write('int main(int argc, char** argv)\n')
                  main_file.write('{\n')
                  main_file.write('   return 0;\n')
                  main_file.write('}\n')
                  main_file.write('\n')

   def _doGitThings(self):

      gitAvaialbale = os.path.exists('.git')

      if self._featureEnabled('git_create') and not gitAvaialbale:
         subprocess.run(['git', 'init'])
         gitAvaialbale = True

      if not gitAvaialbale:
         return

      subprocess.run(['git', 'add', '.gitignore'])
      subprocess.run(['git', 'add', '_clang-format'])
      subprocess.run(['git', 'add', 'CMakeLists.txt'])
      if os.path.exists(f'{self.name}.precompiled.h'):
         subprocess.run(['git', 'add', f'{self.name}.precompiled.h'])
      subprocess.run(['git', 'commit', '-m', '"first commit"'])


if __name__ == '__main__':

   Project.main()
