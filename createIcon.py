#!/usr/bin/env python3

import argparse
import os
import pathlib
import shutil
import subprocess

import xml.etree.ElementTree as et

script_path = pathlib.Path(__file__).parent.resolve()
script_path = str(script_path)


def createIcons(iconNameList):

   root = et.Element('svg')
   root.set('width', '100%')
   root.set('height', '100%')
   root.set('viewBox', '0 0 64 64')
   root.set('version', '1.1')
   root.set('xmlns', 'http://www.w3.org/2000/svg')
   root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
   root.set('xml:space', 'preserve')
   root.set('xmlns:serif', 'http://www.serif.com/')
   root.set('style', 'fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;')

   tree = et.ElementTree(root)
   # docType = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
   et.indent(tree, space=" ", level=0)

   for name in iconNameList:
      if name.endswith('.svg') or name.endswith('.afdesign'):
         continue

      tree.write(name + '.svg', encoding='UTF-8', xml_declaration=True, short_empty_elements=False)
      shutil.copy(script_path + '/Icon.afdesign', name + '.afdesign')


def gatherFromDesktop():

   desktop = str(pathlib.Path.home()) + '/Desktop'

   for entry in os.scandir(desktop):
      if not entry.is_file():
         continue
      if not entry.name.endswith('.svg') and not entry.name.endswith('.afdesign'):
         continue
      print(entry.name)
      shutil.move(entry.path, os.getcwd() + '/' + entry.name)


def addToResourceFile():

   rcFileName = None
   for entry in os.scandir(os.getcwd()):
      if not entry.is_file():
         continue

      if not entry.name.endswith('.qrc'):
         continue

      rcFileName = entry.path
      break

   if not rcFileName:
      print('no qrc file found')
      return

   resourceNameList = list()
   for entry in os.scandir():
      if not entry.is_file():
         continue
      if not entry.name.endswith('.svg'):
         continue
      resourceNameList.append(entry.name)

   if not resourceNameList:
      print('no svg icons found')
      return

   tree = et.parse(rcFileName)
   root = tree.getroot()

   resource = root.find('qresource')

   removeList = list()

   for child in resource:
      if 'file' != child.tag:
         continue
      name = child.text
      if not name in resourceNameList:
         resourceNameList.append(name)
      removeList.append(child)

   for child in removeList:
      resource.remove(child)

   resourceNameList.sort()

   for name in resourceNameList:
      entry = et.SubElement(resource, 'file')
      entry.text = name

   et.indent(tree, space=" ", level=0)
   tree.write(rcFileName, encoding='UTF-8', short_empty_elements=False)


def createIconSet(iconNameList):

   path = script_path + '/icon_set.sh'
   for name in iconNameList:
      subprocess.run([path, name], check=True)


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
