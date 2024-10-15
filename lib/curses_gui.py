#

import curses


class Action:
   NONE = 0
   CREATE = 1
   EXIT = 2


class Color:
   NONE = 0
   SELCTED = 1
   HEADER = 2
   HEADER_HIGHLIGHT = 3
   BANNER = 4
   BANNER_HIGHLIGHT = 5


class CursesGui:

   def __init__(self, screen, maxCursorIndex, bannerHeight=4):

      self._screen = screen
      self._cursorIndex = 0
      self._maxCursorIndex = maxCursorIndex

      self._color_index = 0

      curses.start_color()
      curses.use_default_colors()

      Color.SELCTED = self.setColor(curses.COLOR_BLACK, curses.COLOR_YELLOW)
      Color.HEADER = self.setColor(curses.COLOR_BLACK, curses.COLOR_BLUE)
      Color.HEADER_HIGHLIGHT = self.setColor(curses.COLOR_WHITE, curses.COLOR_BLUE)
      Color.BANNER = self.setColor(curses.COLOR_BLACK, curses.COLOR_YELLOW)
      Color.BANNER_HIGHLIGHT = self.setColor(curses.COLOR_WHITE, curses.COLOR_YELLOW)

      y, x = self._screen.getmaxyx()
      self._header = curses.newwin(1, x, 0, 0)
      self._banner = curses.newwin(bannerHeight, x, y - (bannerHeight + 1), 0)
      self._footer = curses.newwin(1, x, y - 1, 0)
      curses.curs_set(0)

   def exec(self):

      while True:
         self._draw()
         action = self._interaction()
         if Action.EXIT == action:
            return
         elif Action.CREATE == action:
            break

      self.create()

   def setColor(self, foreground, background):

      self._color_index += 1
      curses.init_pair(self._color_index, foreground, background)
      return curses.color_pair(self._color_index)

   def create(self):

      pass

   def toggle(self, index):

      pass

   def fillScreen(self, screen, index):

      pass

   def fillHeader(self, header):

      pass

   def fillBanner(self, banner):

      banner.addstr(0, 1, 'Keyboard usage:', Color.BANNER_HIGHLIGHT)
      banner.addstr(1, 1, '* toogle (space)')
      banner.addstr(2, 1, '* create (c)')
      banner.addstr(3, 1, '* quit (q)')

   def fillFooter(self, footer):

      pass

   def _draw(self):

      self._screen.clear()
      self.fillScreen(self._screen, self._cursorIndex)
      self._screen.refresh()

      self._header.clear()
      self._header.bkgd(Color.HEADER)
      self.fillHeader(self._header)
      self._header.refresh()

      self._banner.clear()
      self._banner.bkgd(Color.BANNER)
      self.fillBanner(self._banner)
      self._banner.refresh()

      self._footer.clear()
      self._footer.bkgd(Color.HEADER)
      self.fillFooter(self._footer)
      self._footer.refresh()

   def _interaction(self):

      match self._screen.getkey():
         case 'q':
            return Action.EXIT
         case 'c':
            return Action.CREATE
         case ' ':
            self.toggle(self._cursorIndex)
         case "KEY_UP":
            if self._cursorIndex > 0:
               self._cursorIndex -= 1
         case "KEY_DOWN":
            if self._cursorIndex + 1 < self._maxCursorIndex:
               self._cursorIndex += 1

      return Action.NONE
