#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyside6",
# ]
# ///

import argparse

from lib.icon import *


def main():

   parser = argparse.ArgumentParser(description='do things with icons.')
   parser.add_argument('iconnames', metavar='ICONS', type=str, nargs='*', help='list of icons to create')
   parser.add_argument('-g', '--gather', action='store_true', help='move all SVG and af files from desktop here')
   parser.add_argument('--create', action='store_true', help='create new SVG icon templates')
   parser.add_argument('--resource', action='store_true', help='add all SVG files to existing resource file')
   parser.add_argument('--set_pc', action='store_true', help='create an PC icon set from a SVG file')

   parser.add_argument('--set_ios', action='store_true', help='create an IOS icon set from a SVG file')
   parser.add_argument('--set_android', action='store_true', help='create an ANDOID icon set from a SVG file')

   args = parser.parse_args()  # will quit here if help is called

   # parse icon names list
   iconNameList = args.iconnames
   if iconNameList and args.create:
      createIcons(iconNameList)
      return

   if args.gather:
      gatherFromDesktop()
      return

   if args.resource:
      addToResourceFile()
      return

   if iconNameList:
      if args.set_pc:
         createIconSetPc(iconNameList)
      if args.set_ios:
         createIconSetIos(iconNameList)
      if args.set_android:
         createIconSetAndroid(iconNameList)
      return

   parser.print_help()


if __name__ == '__main__':
   main()
