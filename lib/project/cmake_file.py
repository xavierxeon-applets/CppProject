#

from PySide6.QtCore import Qt

from ..file_writer import FileWriter


class CMakeFile:

   def __init__(self, project, files_model):

      self.project = project
      self.files_model = files_model

      files_model.registerFile('CMakeLists.txt')

   def generate(self):

      self.files_model.maybeClean('CMakeLists.txt')

      with FileWriter('CMakeLists.txt') as line:
         line(f'cmake_minimum_required(VERSION 3.16)')
         line(f'project({self.project})')
         line(f'set(CMAKE_CXX_STANDARD 17)')
         line(f'set(CMAKE_CXX_STANDARD_REQUIRED ON)')
         line(f'set(CMAKE_CXX_EXTENSIONS OFF)')
