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
