#


import os
import shutil
import subprocess

from PySide6.QtCore import Qt

from ..logger import log
from ..file_writer import FileWriter
from .cmake_file import CMakeFile
from .cpp_files import CppFiles
from .files_model import FilesModel
from .qml_files import QmlFiles
from .defs import *


class Project:

   def __init__(self):

      self.projectPath = os.getcwd()
      self.name = os.path.basename(self.projectPath)

      scriptDir = os.path.abspath(__file__)
      self._scriptDir = os.path.dirname(scriptDir)

      self.files_model = FilesModel(self)

      self.cmake_file = CMakeFile(self, self.files_model)
      self.cpp_files = CppFiles(self, self.files_model)
      self.qml_files = QmlFiles(self, self.files_model)

      self._type = Type.Widgets
      self._target = Target.Application
      self._components = 0
      self._features = Features.PreCompiledHeader | Features.CreateMain

   def typeChanged(self, newType):

      self._type = newType

   def targetChanged(self, newTarget):

      self._target = newTarget

   def componentsChanged(self, newComponents, checked):

      if checked:
         self._components |= newComponents
      else:
         self._components &= ~newComponents

   def featuresChanged(self, newFeatures, checked):

      if checked:
         self._features |= newFeatures
      else:
         self._features &= ~newFeatures

   def _create(self):

      log(f'Creating project {self.name} @ {self.projectPath}')
      os.chdir(self.projectPath)

      self.cmake_file.generate()

      if self._features & Features.CreateMain:
         self.cpp_files.generate()

      if self._features & Features.CreateQmlType:
         self.qml_files.generate()

      shutil.copy(self._scriptDir + '/_clang-format', '_clang-format')
      self._doGitThings()

      log('Project created successfully')
      self.files_model.update()

   def _doGitThings(self):

      with FileWriter('.gitignore') as line:
         line('**/*.user')
         line('**/build')

      gitAvailable = os.path.exists('.git')

      if (self._features & Features.CreateGit) and not gitAvailable:
         log('Initializing git repository')
         subprocess.run(['git', 'init'])
         gitAvailable = True

      if not gitAvailable:
         log('No git repository', Qt.blue)
         return

      log('Adding files to git repository')

      subprocess.run(['git', 'add', '.gitignore', '_clang-format'])
      subprocess.run(['git', 'add', '*'])

      subprocess.run(['git', 'commit', '-m', '"first commit"'])
