#!/usr/bin/env python3


import curses


class Gui:

   def __init__(self):

      pass

   def exec(self, screen):

      self._initColors()

      self.header = curses.newwin(1, curses.COLS - 1, 0, 0)
      curses.curs_set(0)

      while True:
         self._draw(screen)
         if not self._interaction(screen):
            break

   def _initColors(self):

      curses.start_color()
      curses.use_default_colors()

      curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
      Gui.BUTTON_INACTIVE = curses.color_pair(1)

      curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
      Gui.SELECTED = curses.color_pair(2)

      curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
      Gui.HEADER = curses.color_pair(3)

      curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
      Gui.SUCCESS = curses.color_pair(4)

   def _refreshHeader(self):

      self.header.clear()
      self.header.bkgd(Gui.HEADER)
      self.header.addstr(0, 1, "Create CMAKE project")
      self.header.refresh()

   def _draw(self, screen):

      screen.clear()
      screen.addstr(1, 1, "press (q) to quit")
      screen.refresh()
      self._refreshHeader()

   def _interaction(self, screen):

      match screen.getkey():
         case 'q':
            return False

      return True


def main():

   gui = Gui()
   curses.wrapper(gui.exec)


if __name__ == '__main__':
   main()
