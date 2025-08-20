#
from PySide6.QtGui import QStandardItemModel, QStandardItem

import os

from PySide6.QtCore import Qt

from ..logger import log


class FilesModel(QStandardItemModel):

   def __init__(self, project):

      QStandardItemModel.__init__(self)

   def registerFile(self, filePath):

      item = QStandardItem(filePath)

      self.appendRow(item)
      self.update()

   def maybeClean(self, filePath):

      if not os.path.exists(filePath):
         return

      items = self.findItems(filePath, Qt.MatchExactly)
      if not items:
         return

      item = items[0]
      if item.checkState() != Qt.Checked:
         return

      log(f'Removing file {filePath}')
      os.remove(filePath)

   def update(self):

      for row in range(self.rowCount()):
         item = self.item(row)
         filePath = item.text()
         if not os.path.exists(filePath):
            item.setForeground(Qt.gray)
            item.setCheckable(False)
         else:
            item.setForeground(Qt.black)
            item.setCheckable(True)
