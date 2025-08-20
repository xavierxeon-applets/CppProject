#!/usr/bin/env python3

import argparse

from lib.file import *


def main():

   parser = argparse.ArgumentParser(description='Create new C++ classes.')

   classGroup = parser.add_argument_group('class creation')
   classGroup.add_argument('classnames', metavar='CLASSES', type=str, nargs='*', help='list of classes to create')
   classGroup.add_argument('-n', '--namespace', action='append', help='all classes are in this namespace (you can use several -n options)')
   classGroup.add_argument('-i', '--inline', action='store_true', help='create HPP file')
   classGroup.add_argument('-s', '--nosource', action='store_true', help='only create header')

   helperGroup = parser.add_argument_group('helper')
   helperGroup.add_argument('-e', '--export', action='append', help='create export header')

   args = parser.parse_args()  # will quit here if help is called

   classNames = args.classnames
   nameSpaces = args.namespace
   inline = args.inline
   nosource = args.nosource
   export = args.export

   if export:
      createExportheader(export)
   else:
      for className in classNames:
         createHeader(className, nameSpaces, inline)
         if inline:
            createInline(className, nameSpaces)
         elif not nosource:
            createSource(className, nameSpaces)


if __name__ == '__main__':
   main()
