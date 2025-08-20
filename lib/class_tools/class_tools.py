#

import os
import sys


def _compileFileBae(className, nameSpaces):

   if nameSpaces:
      return ''.join(nameSpaces) + className
   else:
      return className


def _compileFullNameSpace(nameSpaces):

   if nameSpaces:
      return '::'.join(nameSpaces) + '::'
   else:
      return ''


def _abortIfExists(fileName):

   if not os.path.exists(fileName):
      return

   print(fileName, 'already exists')
   sys.exit(1)


def createHeader(className, nameSpaces, inline):

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.h'
   _abortIfExists(fileName)

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
      fprint(f'{className}();')
      indent -= 1
      fprint('};')

      if nameSpaces:
         for nameSpace in reversed(nameSpaces):
            indent -= 1
            fprint(f'\u007d // namespace {nameSpace}')

      if inline:
         fprint('')
         fprint(f'#ifndef {fileBase}HPP')
         fprint(f'#include "{fileBase}.hpp"')
         fprint(f'#endif // NOT {fileBase}HPP')

      fprint('')
      fprint(f'#endif // NOT {fileBase}H')


def createSource(className, nameSpaces):

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.cpp'
   _abortIfExists(fileName)

   nameSpace = _compileFullNameSpace(nameSpaces)

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

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.hpp'
   _abortIfExists(fileName)

   nameSpace = _compileFullNameSpace(nameSpaces)

   with open(fileName, 'w') as outfile:

      def fprint(line):
         outfile.write(line + '\n')

      fprint(f'#ifndef {fileBase}HPP')
      fprint(f'#define {fileBase}HPP')
      fprint('')
      fprint(f'#include "{fileBase}.h"')
      fprint('')

      fprint(f'inline {nameSpace}{className}::{className}()')
      fprint('{')
      fprint('}')

      fprint('')
      fprint(f'#endif // NOT {fileBase}HPP')
      fprint('')


def createExportheader(exportNames):

   for name in exportNames:
      macroName = name.upper()

      with open(f'{name}ExportDef.h', 'w') as outfile:

         def fprint(line):
            outfile.write(line + '\n')

         fprint(f'#ifndef {name}ExportDefH')
         fprint(f'#define {name}ExportDefH')
         fprint('')
         fprint('// clang-format off')
         fprint('#if defined(__unix) || defined(__QNXNTO__) || defined(__APPLE__)')
         fprint(f'   #define {macroName}_DECLSPEC')
         fprint('#else')
         fprint(f'   #ifdef EXTENSION_{macroName}')
         fprint(f'      #define {macroName}_DECLSPEC __declspec(dllexport)')
         fprint('   #else')
         fprint(f'      #define {macroName}_DECLSPEC __declspec(dllimport)')
         fprint('   #endif')
         fprint('#endif')
         fprint('// clang-format on')
         fprint('')
         fprint(f'#endif // NOT {name}ExportDefH')
         fprint('')
