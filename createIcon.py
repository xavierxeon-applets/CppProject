#!/usr/bin/env python3

import argparse
import os
import xml.etree.ElementTree as et


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
    #docType = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    et.indent(tree, space=" ", level=0)

    for name in iconNameList:
        tree.write(name, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)


def addToResourceFile(iconNameList):

    fileName = None
    for entry in os.scandir(os.getcwd()):
        if not entry.is_file():
            continue

        if not entry.name.endswith('.qrc'):
            continue

        fileName = entry.path
        break

    if not fileName:
        return

    tree = et.parse(fileName)
    root = tree.getroot()

    resource = root.find('qresource')

    removeList = list()

    for child in resource:
        if 'file' != child.tag:
            continue
        name = child.text
        if not name in iconNameList:
            iconNameList.append(name)
        removeList.append(child)

    for child in removeList:
        resource.remove(child)

    iconNameList.sort()

    for name in iconNameList:
        entry = et.SubElement(resource, 'file')
        entry.text = name

    et.indent(tree, space=" ", level=0)
    tree.write(fileName, encoding='UTF-8', short_empty_elements=False)


def main():

    parser = argparse.ArgumentParser(description='Create new SVG icon templates.')
    parser.add_argument('iconnames', metavar='ICONS', type=str, nargs='+', help='list of icons to create')
    parser.add_argument('-a', '--add', action='store_true', help='add to resource file (if it exists')

    args = parser.parse_args()  # will quit here if help is called

    iconNameList = args.iconnames
    for index in range(len(iconNameList)):
        name = iconNameList[index]
        if name.endswith('.svg'):
            continue
        iconNameList[index] = name + '.svg'

    createIcons(iconNameList)

    if args.add:
        addToResourceFile(iconNameList)


if __name__ == '__main__':
    main()
