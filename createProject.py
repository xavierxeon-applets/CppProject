#!/usr/bin/env python3


import signal
import sys

try:
   from PySide6.QtWidgets import QApplication
   from PySide6.QtCore import QTimer, QSettings
except ImportError:
   print("pip3 install --user --upgrade pyside6")
   sys.exit(1)

from wapy.qt_tools import autoUIC


def signit_handler(*args):

   QApplication.quit()


if __name__ == '__main__':

   # Project.main()

   QApplication.setApplicationName('CppProjectCreator')
   QApplication.setOrganizationName('Schweinesystem')
   QApplication.setOrganizationDomain('schweinesystem.ddns.net')

   app = QApplication([])

   QSettings.setDefaultFormat(QSettings.IniFormat)
   settings = QSettings()
   print(f'Settings @ {settings.fileName()}')

   signal.signal(signal.SIGINT, signit_handler)
   timer = QTimer()
   timer.start(500)
   timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

   autoUIC()
   from lib.project_tools import MainWidget

   mw = MainWidget()
   mw.show()

   sys.exit(app.exec())
