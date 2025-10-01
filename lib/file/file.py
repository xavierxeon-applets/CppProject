#


from ..file_writer import FileWriter


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


def createHeader(className, nameSpaces, inline):

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.h'

   with FileWriter(fileName) as line:

      line(f'#ifndef {fileBase}H')
      line(f'#define {fileBase}H')
      line()

      if nameSpaces:
         for nameSpace in nameSpaces:
            line(f'namespace {nameSpace}')
            line('{')
            line.indent(1)

      line(f'class {className}')
      line('{')
      line('public:')
      line(f'   {className}();')
      line('};')

      if nameSpaces:
         for nameSpace in reversed(nameSpaces):
            line.indent(-1)
            line(f'\u007d // namespace {nameSpace}')

      if inline:
         line()
         line(f'#ifndef {fileBase}HPP')
         line(f'#include "{fileBase}.hpp"')
         line(f'#endif // NOT {fileBase}HPP')

      line()
      line(f'#endif // NOT {fileBase}H')


def createSource(className, nameSpaces):

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.cpp'

   nameSpace = _compileFullNameSpace(nameSpaces)

   with FileWriter(fileName) as line:

      line(f'#include "{fileBase}.h"')
      line()
      line(f'{nameSpace}{className}::{className}()')
      line('{')
      line('}')
      line()


def createInline(className, nameSpaces):

   fileBase = _compileFileBae(className, nameSpaces)
   fileName = fileBase + '.hpp'

   nameSpace = _compileFullNameSpace(nameSpaces)

   with FileWriter(fileName) as line:

      line(f'#ifndef {fileBase}HPP')
      line(f'#define {fileBase}HPP')
      line()
      line(f'#include "{fileBase}.h"')
      line()

      line(f'inline {nameSpace}{className}::{className}()')
      line('{')
      line('}')

      line()
      line(f'#endif // NOT {fileBase}HPP')
      line()


def createExportheader(exportNames):

   for name in exportNames:

      with FileWriter(f'{name}ExportDef.h') as line:

         macroName = name.upper()

         line(f'#ifndef {name}ExportDefH')
         line(f'#define {name}ExportDefH')
         line('')
         line('// clang-format off')
         line('#if defined(__unix) || defined(__QNXNTO__) || defined(__APPLE__)')
         line(f'   #define {macroName}_DECLSPEC')
         line('#else')
         line(f'   #ifdef EXTENSION_{macroName}')
         line(f'      #define {macroName}_DECLSPEC __declspec(dllexport)')
         line('   #else')
         line(f'      #define {macroName}_DECLSPEC __declspec(dllimport)')
         line('   #endif')
         line('#endif')
         line('// clang-format on')
         line('')
         line(f'#endif // NOT {name}ExportDefH')
         line('')
