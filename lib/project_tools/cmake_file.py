#

class CMakeFile:

   def __init__(self, project):

      self.project = project

   def generate(self):

      with open('CMakeLists.txt', 'w') as cmakefile:
         cmakefile.write('hello')
