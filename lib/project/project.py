#

from enum import IntEnum, IntFlag, auto
import os
import shutil
import subprocess

from .cmake_file import CMakeFile
from .cpp_files import CppFiles
from ..logger import log


class Project:

   class Type(IntEnum):
      Widgets = 0
      QML = 1
      Cpp = 2

   class Target(IntEnum):
      Application = 0
      SharedLibrary = 1
      StaticLibrary = 2

   class Components(IntFlag):
      Network = auto()

   class Features(IntFlag):
      PreCompiledHeader = auto()
      AppIcon = auto()
      CreateMain = auto()
      CreateGit = auto()

   def __init__(self):

      self.projectPath = os.getcwd()
      self.name = os.path.basename(self.projectPath)

      scriptDir = os.path.abspath(__file__)
      self._scriptDir = os.path.dirname(scriptDir)

      self._type = Project.Type.Widgets
      self._target = Project.Target.Application
      self._components = 0
      self._features = Project.Features.PreCompiledHeader | Project.Features.CreateMain

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

      cmake_file = CMakeFile(self)
      cmake_file.generate()

      cpp_files = CppFiles(self)
      cpp_files.generate()

      shutil.copy(self._scriptDir + '/_clang-format', '_clang-format')
      self._doGitThings()

   def _doGitThings(self):

      with open('.gitignore', 'w') as gitignore:
         gitignore.write('/bin\n')
         gitignore.write('**/*.user\n')
         gitignore.write('**/build\n')

      gitAvaialbale = os.path.exists('.git')

      if (self._features & Project.Features.CreateGit) and not gitAvaialbale:
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
