#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyside6",
# ]
# ///

import argparse

from lib.qml import *

def main():

   parser = argparse.ArgumentParser(description='create qml files.')
   parser.add_argument('qmlnames', metavar='QML FILES', type=str, nargs='*', help='list of qml files to create')

   args = parser.parse_args()  # will quit here if help is called

   qmlNames = args.qmlnames
   for fileName in qmlNames:
      createQml(fileName)
   

if __name__ == '__main__':
   main()