#
import os

from PySide6.QtCore import Qt

from .logger import log


class FileWriter:

   def __init__(self, fileName):

      self._fileName = fileName
      self._file = None
      self._indent = 0

   def __enter__(self):

      if os.path.exists(self._fileName):
         log(f'File {self._fileName} already exists', Qt.red)
      else:
         self._file = open(self._fileName, 'w')
      return self

   def __exit__(self, *args):

      if not self._file:
         return

      log(f'Created file {self._fileName}', Qt.green)
      self._file.close()

   def __call__(self, content=None):

      if not self._file:
         return

      if content:
         self._file.write(' ' * 3 * self._indent + content + '\n')
      else:
         self._file.write('\n')

   def indent(self, value=0):

      self._indent += value
