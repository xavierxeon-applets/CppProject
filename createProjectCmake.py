#!/usr/bin/env python3

import curses
import os

from lib import Color, CursesGui


class Project(CursesGui):

   def __init__(self, screen):

      self.projectPath = os.getcwd()
      self.name = os.path.basename(self.projectPath)

      scriptDir = os.path.abspath(__file__)
      self.scriptDir = os.path.dirname(scriptDir)

      self.features = {'app_wrapper': [True, 'Mac and Windows app'],
                       'icon': [False, 'App icon'],
                       'gui': [False, 'Gui'],
                       'widget': [True, 'Widgets'],
                       'network': [False, 'Network']}

      super().__init__(screen, len(self.features))

   def create(self):

      pass

   def toggle(self, index):

      keys = list(self.features.keys())
      key = keys[index]
      feature = self.features[key]
      feature[0] = not feature[0]

   def fillScreen(self, screen, index):

      screen.addstr(2, 1, 'Qt Features:')
      lineOffset = 4

      line = 0
      for _, feature in self.features.items():
         check = '[x]' if feature[0] else '[ ]'
         checkColor = Color.SELCTED if index == line else 0
         screen.addstr(line + lineOffset, 1, check, checkColor)
         screen.addstr(line + lineOffset, 5, feature[1])
         line += 1

   def fillHeader(self, header):

      header.addstr(0, 1, 'Create CMAKE project for ')
      header.addstr(0, 26, self.name, Color.HEADER_HIGHLIGHT)

   def fillFooter(self, footer):

      footer.addstr(0, 1, self.projectPath + ' - ' + self.scriptDir)


def main(screen):

   project = Project(screen)
   project.exec()


if __name__ == '__main__':
   curses.wrapper(main)
