#!/usr/bin/env python3

import os
import sys
import argparse

def createHeader(inletCount, outletCount):

    text = '// inlets and outlets\n'

    text += f'inlets = {inletCount};\n'
    for index in range(inletCount):
        text += f'setinletassist({index}, "text");\n'
    text += '\n'

    text += f'outlets = {outletCount};\n'
    for index in range(outletCount):
        text += f'setoutletassist({index}, "text");\n'
    text += '\n'

    return text

def createBody():

    text = 'function bang(){\n'
    text += '   post("bang");\n'
    text += '}\n'
    text += '\n'

    return text

def createBodyUi():

    text = 'function bang(){\n'
    text += '   post("bang");\n'
    text += '}\n'
    text += '\n'

    return text

def main():

    parser = argparse.ArgumentParser(description='Create new Max javascript.')
    parser.add_argument('scriptname', metavar='SCRIPT', type=str, nargs=1, help='name of script to create')
    parser.add_argument('-i', '--inlet', metavar='COUNT', nargs='?', default=0, help='number of inlets')
    parser.add_argument('-o', '--outlet', metavar='COUNT', nargs='?', default=0, help='number of outlets')
    parser.add_argument('-u', '--ui', action='store_true', help='create ui file')

    args = parser.parse_args()  # will quit here if help is called
    scriptname = args.scriptname[0]
    if not scriptname.endspwith('.js'):
        scriptname += '.js'

    if os.path.exists(scriptname):
        print(f'script {scriptname} does already exist')
        return
    
    inletCount = int(args.inlet)
    outletCount = int(args.outlet)

    text = createHeader(inletCount, outletCount)

    if args.ui:
        text += createBodyUi()
    else:
        text += createBody()

    with open(scriptname, 'w') as outfile:
        outfile.write(text)

if __name__ == '__main__':
    main()
