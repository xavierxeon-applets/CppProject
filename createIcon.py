#!/usr/bin/env python3

import argparse


from lib.icon import *


def main():

   parser = argparse.ArgumentParser(description='do things with icons.')
   parser.add_argument('iconnames', metavar='ICONS', type=str, nargs='*', help='list of icons to create')
   parser.add_argument('-c', '--create', action='store_true', help='create new SVG icon templates')
   parser.add_argument('-g', '--gather', action='store_true', help='move all SVG and afdesign files from desktop here')
   parser.add_argument('-r', '--resource', action='store_true', help='add all SVG files to existing resource file')
   parser.add_argument('-s', '--set', action='store_true', help='create an icon set from a SVG file')

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

   if iconNameList and args.set:
      createIconSet(iconNameList)
      return

   parser.print_help()


if __name__ == '__main__':
   main()
