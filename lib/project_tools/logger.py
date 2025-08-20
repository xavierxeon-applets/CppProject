#

from PySide6.QtCore import Qt


class Logger:

   me = None

   def __init__(self, textEdit):

      Logger.me = self
      self.textEdit = textEdit

   def __del__(self):
      Logger.me = None

   def print(self, message, color):

      if color:
         self.textEdit.setTextColor(color)
      else:
         self.textEdit.setTextColor(Qt.black)

      self.textEdit.append(message)


@staticmethod
def log(message, color=None):

   if not Logger.me:
      print(message)
      return

   Logger.me.print(message, color)
