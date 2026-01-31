#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyside6",
# ]
# ///

import signal
import sys

from wapy.qt_tools import autoUIC


def signit_handler(*args):

   QApplication.quit()


if __name__ == '__main__':

   app = QApplication([])

   signal.signal(signal.SIGINT, signit_handler)
   timer = QTimer()
   timer.start(500)
   timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

   autoUIC()
   from lib.project import MainWidget

   mw = MainWidget()
   mw.show()

   sys.exit(app.exec())
