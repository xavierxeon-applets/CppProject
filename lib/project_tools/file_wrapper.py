#
import os

from PySide6.QtCore import Qt

from .logger import log


class FileWrapper:

   def __init__(self, fileName):

      self.fileName = fileName
      self.file = None

   def __enter__(self):

      if os.path.exists(self.fileName):
         log(f'File {self.fileName} already exists', Qt.red)
      else:
         log(f'Opening file {self.fileName}')
         self.file = open(self.fileName, 'w')
      return self.line

   def __exit__(self, *args):

      if not self.file:
         return

      log(f'Closing file {self.fileName}')
      self.file.close()

   def line(self, content=None):

      if not self.file:
         return

      if content:
         self.file.write(content + '\n')
      else:
         self.file.write('\n')
