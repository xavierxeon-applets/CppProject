#
from PySide6.QtWidgets import QWidget
from .project import Project
from .mainwidget_ui import Ui_MainWidget

from PySide6.QtWidgets import QButtonGroup

from ..logger import Logger
from .defs import *


class MainWidget(QWidget, Project, Ui_MainWidget):

   def __init__(self):

      QWidget.__init__(self)
      self.setupUi(self)

      self.setWindowTitle(f'Create Project [{self.name}]')
      self.logger = Logger(self.logEdit)

      Project.__init__(self)

      self.overwriteTree.setModel(self.files_model)

      typeButton = QButtonGroup(self)
      typeButton.setExclusive(True)
      typeButton.idClicked.connect(self.typeChanged)

      typeButton.addButton(self.widgetsRadio, Type.Widgets)
      typeButton.addButton(self.qmlRadio, Type.QML)
      typeButton.addButton(self.cppRadio, Type.Cpp)

      targetButton = QButtonGroup(self)
      targetButton.setExclusive(True)
      targetButton.idClicked.connect(self.targetChanged)

      targetButton.addButton(self.appRadio, Target.Application)
      targetButton.addButton(self.sharedLibRadio, Target.SharedLibrary)
      targetButton.addButton(self.staticLibRadio, Target.StaticLibrary)

      componentsButton = QButtonGroup(self)
      componentsButton.setExclusive(False)
      componentsButton.idToggled.connect(self.componentsChanged)

      componentsButton.addButton(self.compNetworkCheck, Components.Network)

      featuresButton = QButtonGroup(self)
      featuresButton.setExclusive(False)
      featuresButton.idToggled.connect(self.featuresChanged)

      featuresButton.addButton(self.precompiledCheck, Features.PreCompiledHeader)
      featuresButton.addButton(self.iconCheck, Features.AppIcon)
      featuresButton.addButton(self.mainCheck, Features.CreateMain)
      featuresButton.addButton(self.gitCheck, Features.CreateGit)
      featuresButton.addButton(self.qmlDummyCheck, Features.CreateQmlType)

      self.startButton.clicked.connect(self.create)  # can not call create of project directly

   def create(self):

      self.logEdit.clear()
      self._create()
