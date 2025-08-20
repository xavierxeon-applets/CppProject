#

from ..file_wrapper import FileWrapper


class CMakeFile:

   def __init__(self, project):

      self.project = project

   def generate(self):

      with FileWrapper('CMakeLists.txt') as line:
         line(f'cmake_minimum_required(VERSION 3.16)')
         line(f'project({self.project})')
         line(f'set(CMAKE_CXX_STANDARD 17)')
         line(f'set(CMAKE_CXX_STANDARD_REQUIRED ON)')
         line(f'set(CMAKE_CXX_EXTENSIONS OFF)')
