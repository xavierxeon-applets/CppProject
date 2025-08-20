#

from PySide6.QtCore import Qt
from cv2 import line

from ..file_writer import FileWriter
from .defs import *


class CMakeFile:

   def __init__(self, project, files_model):

      self.project = project
      self.files_model = files_model

      files_model.registerFile('CMakeLists.txt')

   def generate(self):

      self.files_model.maybeClean('CMakeLists.txt')
      with FileWriter('CMakeLists.txt') as line:
         self.writeHeader(line)
         if self.project._type == Type.Cpp:
            self.writeCppPart(line)
         elif self.project._type == Type.QML:
            self.writeQmlPart(line)
         else:
            self.writeWidgetsPart(line)

   def writeHeader(self, line):

      line('cmake_minimum_required(VERSION 3.20)')
      line(f'project({self.project.name} LANGUAGES CXX)')
      line()

      line('set(CMAKE_CXX_STANDARD 20)')
      line('set(CMAKE_CXX_STANDARD_REQUIRED ON)')
      line('set(CMAKE_CXX_EXTENSIONS ON)')
      line()

      line('if(NOT CMAKE_BUILD_TYPE)')
      line('   set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)')
      line('endif()')
      line('message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")')
      line()

   def writeCppPart(self, line):

      line('find_package(WaTools REQUIRED)')
      line()

      line('# c++')
      line('include_directories(${CMAKE_CURRENT_SOURCE_DIR})')
      line()
      line('file(GLOB SOURCE_FILES')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.h')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp')
      line(')')
      line()

      if self.project._target & Target.SharedLibrary:
         line('add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})')
      elif self.project._target & Target.StaticLibrary:
         line('add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})')
      else:
         line('add_executable(${PROJECT_NAME} ${SOURCE_FILES})')

      if self.project._features & Features.PreCompiledHeader:
         line('use_precompiled_headers()')
         line()

   def writeQmlPart(self, line):

      components = ['Quick', 'Svg']
      if self.project._components & Components.Network:
         components.append('Network')
      componentsList = ' '.join(components)

      line(f'find_package(Qt6 REQUIRED COMPONENTS {componentsList})')
      line('set(CMAKE_AUTOMOC ON)')
      line('set(CMAKE_AUTORCC ON)')
      line()
      line('find_package(WaTools REQUIRED)')
      line()

      line('# c++')
      line('include_directories(${CMAKE_CURRENT_SOURCE_DIR})')
      line()
      line('file(GLOB SOURCE_FILES')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.h')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp')
      line(')')
      line()

      if self.project._target & Target.SharedLibrary:
         line('qt_add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})')
      elif self.project._target & Target.StaticLibrary:
         line('qt_add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})')
      else:
         line('qt_add_executable(${PROJECT_NAME} ${SOURCE_FILES})')

      if self.project._features & Features.PreCompiledHeader:
         line('use_precompiled_headers()')
         line()

      if self.project._features & Features.AppIcon:
         line('set_application_icon(${CMAKE_CURRENT_SOURCE_DIR}/Resources/${PROJECT_NAME})')
      else:
         line('set_application_no_icon()')
      line()

      componentsList = ' Qt6::'.join(components)
      componentsList = 'Qt6::' + componentsList
      line(f'target_link_libraries(${{PROJECT_NAME}} PRIVATE {componentsList})')
      line()

      line('# QML')
      if self.project._features & Features.CreateQmlType:
         line('add_qml_module_dir(QmlTypes Display)')
      line('add_qml_sources(Gui)')
      line()

   def writeWidgetsPart(self, line):

      components = ['Widgets', 'Svg']
      if self.project._components & Components.Network:
         components.append('Network')
      componentsList = ' '.join(components)

      line(f'find_package(Qt6 REQUIRED COMPONENTS {componentsList})')
      line('set(CMAKE_AUTOMOC ON)')
      line('set(CMAKE_AUTOUIC ON)')
      line('set(CMAKE_AUTORCC ON)')
      line()
      line('find_package(WaTools REQUIRED)')
      line()

      line('# c++')
      line('include_directories(${CMAKE_CURRENT_SOURCE_DIR})')
      line()
      line('file(GLOB SOURCE_FILES')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.h')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.ui')
      line('   ${CMAKE_CURRENT_SOURCE_DIR}/*.qrc')
      line(')')
      line()

      line('add_all_subdirs_files(${CMAKE_CURRENT_SOURCE_DIR})')
      line()

      if self.project._target & Target.SharedLibrary:
         line('qt_add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})')
      elif self.project._target & Target.StaticLibrary:
         line('qt_add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})')
      else:
         line('qt_add_executable(${PROJECT_NAME} ${SOURCE_FILES})')

      if self.project._features & Features.PreCompiledHeader:
         line('use_precompiled_headers()')
         line()

      if self.project._features & Features.AppIcon:
         line('set_application_icon(${CMAKE_CURRENT_SOURCE_DIR}/Resources/${PROJECT_NAME})')
      else:
         line('set_application_no_icon()')
      line()

      componentsList = ' Qt6::'.join(components)
      componentsList = 'Qt6::' + componentsList
      line(f'target_link_libraries(${{PROJECT_NAME}} PRIVATE {componentsList})')
      line()

      if self.project._features & Features.CreateQmlType:
         line('# QML')
         line('add_qml_module_dir(QmlTypes Display)')
         line()
