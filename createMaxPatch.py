#!/usr/bin/env python3

import os
import json
import argparse


def createInlets(inletCount):

    inlets = list()
    if inletCount <= 0:
        return inlets

    for index in range(inletCount):
        box = dict()
        box['maxclass'] = 'inlet'
        box['patching_rect'] = [20.0 + (index * 40), 20.0, 30.0, 30.0]

        inlet = {'box': box}
        inlets.append(inlet)

    return inlets


def createOutlets(outletCount):

    outlets = list()
    if outletCount <= 0:
        return outlets

    for index in range(outletCount):
        box = dict()
        box['maxclass'] = 'outlet'
        box['patching_rect'] = [20.0 + (index * 40), 200.0, 30.0, 30.0]

        outlet = {'box': box}
        outlets.append(outlet)

    return outlets


def main():

    parser = argparse.ArgumentParser(description='Create new Max patch.')
    parser.add_argument('patchname', metavar='PATCH', type=str, nargs=1, help='name of patch to create')
    parser.add_argument('-i', '--inlet', metavar='COUNT', nargs='?', default=1, help='number of inlets, default is 1')
    parser.add_argument('-o', '--outlet', metavar='COUNT', nargs='?', default=1, help='number of outlets, default is 1')

    args = parser.parse_args()  # will quit here if help is called

    patchname = args.patchname[0]
    if not patchname.endswith('.maxpat'):
        patchname += '.maxpat'

    if os.path.exists(patchname):
        print(f'patch {patchname} does already exist')
        return

    inletCount = int(args.inlet)
    outletCount = int(args.outlet)

    boxes = list()
    for inlet in createInlets(inletCount):
        boxes.append(inlet)
    for outlet in createOutlets(outletCount):
        boxes.append(outlet)

    with open(patchname, 'w') as outfile:
        data = {'patcher': {'boxes': boxes}}
        json.dump(data, outfile, indent=3)


if __name__ == '__main__':
    main()
