#

import curses


class KeyAction:

   def __init__(self, function, exitLoop, helpText):

      self.function = function
      self.exitLoop = exitLoop
      self.helpText = helpText


class PredfinedColor:
   NONE = 0
   SELCTED = 1
   HEADER = 2
   HEADER_HIGHLIGHT = 3
   BANNER = 4
   BANNER_HIGHLIGHT = 5


class CursesGui:

   def __init__(self, screen, maxCursorIndex, keyMap, bannerHeight=None):

      self._screen = screen
      self._keyMap = keyMap
      if not bannerHeight:
         bannerHeight = 1 + len(self._keyMap) 

      self._cursorIndex = 0
      self._maxCursorIndex = maxCursorIndex

      self._color_index = 0

      curses.start_color()
      curses.use_default_colors()

      PredfinedColor.SELCTED = self.setColor(curses.COLOR_BLACK, curses.COLOR_MAGENTA)
      PredfinedColor.HEADER = self.setColor(curses.COLOR_BLACK, curses.COLOR_BLUE)
      PredfinedColor.HEADER_HIGHLIGHT = self.setColor(curses.COLOR_WHITE, curses.COLOR_BLUE)
      PredfinedColor.BANNER = self.setColor(curses.COLOR_BLACK, curses.COLOR_MAGENTA)
      PredfinedColor.BANNER_HIGHLIGHT = self.setColor(curses.COLOR_WHITE, curses.COLOR_MAGENTA)

      y, x = self._screen.getmaxyx()
      self._header = curses.newwin(1, x, 0, 0)
      self._banner = curses.newwin(bannerHeight, x, y - (bannerHeight + 1), 0)
      self._footer = curses.newwin(1, x, y - 1, 0)
      curses.curs_set(0)


   def exec(self):

      while True:
         self._draw()
         if self._interaction():
            return

   def setColor(self, foreground, background):

      self._color_index += 1
      curses.init_pair(self._color_index, foreground, background)
      return curses.color_pair(self._color_index)

   def fillScreen(self, screen, index):

      pass

   def fillHeader(self, header):

      pass

   def fillBanner(self, banner):

      banner.addstr(0, 1, 'Keyboard usage:', PredfinedColor.BANNER_HIGHLIGHT)
      line = 1
      for key, action in self._keyMap.items():
         if ' ' == key:
            key = 'space'
         banner.addstr(line, 1, f'* {action.helpText} ({key})')
         line += 1

   def fillFooter(self, footer):

      pass

   def _draw(self):

      self._screen.clear()
      self.fillScreen(self._screen, self._cursorIndex)
      self._screen.refresh()

      self._header.clear()
      self._header.bkgd(PredfinedColor.HEADER)
      self.fillHeader(self._header)
      self._header.refresh()

      self._banner.clear()
      self._banner.bkgd(PredfinedColor.BANNER)
      self.fillBanner(self._banner)
      self._banner.refresh()

      self._footer.clear()
      self._footer.bkgd(PredfinedColor.HEADER)
      self.fillFooter(self._footer)
      self._footer.refresh()

   def _interaction(self):

      k = self._screen.getkey()
      if k in self._keyMap:
         action = self._keyMap[k]   
         if action.function:
            action.function(self._cursorIndex)
         return action.exitLoop      
      elif k ==  "KEY_UP":
         if self._cursorIndex > 0:
            self._cursorIndex -= 1
      elif k ==  "KEY_DOWN":
         if self._cursorIndex + 1 < self._maxCursorIndex:
            self._cursorIndex += 1

      return False
