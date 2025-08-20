#
from enum import IntEnum, IntFlag, auto


class Type(IntEnum):
   Widgets = 0
   QML = 1
   Cpp = 2


class Target(IntEnum):
   Application = 0
   SharedLibrary = 1
   StaticLibrary = 2


class Components(IntFlag):
   Network = auto()


class Features(IntFlag):
   PreCompiledHeader = auto()
   AppIcon = auto()
   CreateMain = auto()
   CreateGit = auto()
   CreateQmlType = auto()
