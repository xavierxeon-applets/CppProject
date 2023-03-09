#!/usr/bin/env python3

import os
import sys
import argparse

def main():

    parser = argparse.ArgumentParser(description='Create new Max javascript.')
    parser.add_argument('scriptname', metavar='SCRIPT', type=str, nargs='1', help='name of script to create')
    parser.add_argument('-i', '--inlet', nargs='1', default=0, help='number of inlets')
    parser.add_argument('-o', '--outlet', nargs='1', default=0, help='number of outlets')
    parser.add_argument('-u', '--ui', action='store_true', help='create ui file')

    args = parser.parse_args()  # will quit here if help is called

 

if __name__ == '__main__':
    main()