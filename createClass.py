#!/usr/bin/env python3

import os, sys, argparse


def fullName(className, nameSpaces):

   if nameSpaces:
      return ''.join(nameSpaces) + className
   else:
      return className

def fullNameSpace(nameSpaces):

   if nameSpaces:
      return '::'.join(nameSpaces) + '::'
   else:
      return ''

def abortIfExists(fileName):

   if not os.path.exists(fileName):
      return

   print(fileName, 'already exists')
   sys.exit(1)


def createHeader(className, nameSpaces, inline):

   fileBase = fullName(className, nameSpaces)
   fileName =  fileBase + '.h'
   abortIfExists(fileName)

   indent = 0
   with open(fileName, 'w') as outfile:

      def fprint(line):
         outfile.write(' ' * 3 * indent + line + '\n')

      fprint(f'#ifndef {fileBase}H')
      fprint(f'#define {fileBase}H')
      fprint('')

      if nameSpaces:
         for nameSpace in nameSpaces:
            fprint(f'namespace {nameSpace}')
            fprint('{')
            indent += 1

      fprint(f'class {className}')
      fprint('{')
      fprint('public:')
      indent += 1
      if inline:
         fprint(f'inline {className}();')
      else:
         fprint(f'{className}();')
      indent -= 1
      fprint('};')

      if nameSpaces:
         for nameSpace in nameSpaces:
            indent -= 1
            fprint(f'\u007d //{nameSpace}')

      if inline:
         fprint('')
         fprint(f'#include "{fileBase}.hpp"')

      fprint('')
      fprint(f'#endif // {fileBase}H')

def createSource(className, nameSpaces):

   fileBase = fullName(className, nameSpaces)   
   fileName = fileBase + '.cpp'
   abortIfExists(fileName)

   nameSpace = fullNameSpace(nameSpaces)
  
   with open(fileName, 'w') as outfile:

      def fprint(line):
         outfile.write(line + '\n')

      fprint(f'#include "{fileBase}.h"')
      fprint('')
      fprint(f'{nameSpace}{className}::{className}()')
      fprint('{')
      fprint('}')
      fprint('')      
   
def createInline(className, nameSpaces):
   
   fileBase = fullName(className, nameSpaces)   
   fileName = fileBase + '.hpp'
   abortIfExists(fileName)

   nameSpace = fullNameSpace(nameSpaces)

   indent = 0
   with open(fileName, 'w') as outfile:

      def fprint(line):
         outfile.write(' ' * 3 * indent + line + '\n')

      fprint(f'#ifndef {fileBase}HPP')
      fprint(f'#define {fileBase}HPP')
      fprint('')         
      fprint(f'#include "{fileBase}.h"')
      fprint('')

      fprint(f'{nameSpace}{className}::{className}()')
      fprint('{')
      fprint('}')
      
      fprint('')
      fprint(f'#endif // {fileBase}HPP')      

def main():

   parser = argparse.ArgumentParser(description = 'Create new C++ classes.')
   parser.add_argument('classnames', metavar='CLASSES', type = str, nargs = '+', help = 'list of classes to create')
   parser.add_argument('-n', '--namespace', action='append', help = 'all classes are in this namespace')
   parser.add_argument('-i', '--inline', action = 'store_true', help = 'create HPP instead of CPP')
      
   args = parser.parse_args() # will quit here if help is called

   classNames = args.classnames
   nameSpaces = args.namespace  
   inline = args.inline

   for className in classNames:

      createHeader(className, nameSpaces, inline)
      if inline:
         createInline(className, nameSpaces)
      else:
         createSource(className, nameSpaces)
  
if __name__ == '__main__':
   main()