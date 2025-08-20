#
from PySide6.QtWidgets import QWidget
from .project import Project
from .mainwidget_ui import Ui_MainWidget

from PySide6.QtWidgets import QButtonGroup

from ..logger import Logger


class MainWidget(QWidget, Project, Ui_MainWidget):

   def __init__(self):

      QWidget.__init__(self)
      self.setupUi(self)

      self.setWindowTitle(f'Create Project [{self.name}]')
      self.logger = Logger(self.logEdit)

      Project.__init__(self)

      typeButton = QButtonGroup(self)
      typeButton.setExclusive(True)
      typeButton.idClicked.connect(self.typeChanged)

      typeButton.addButton(self.widgetsRadio, Project.Type.Widgets)
      typeButton.addButton(self.qmlRadio, Project.Type.QML)
      typeButton.addButton(self.cppRadio, Project.Type.Cpp)

      targetButton = QButtonGroup(self)
      targetButton.setExclusive(True)
      targetButton.idClicked.connect(self.targetChanged)

      targetButton.addButton(self.appRadio, Project.Target.Application)
      targetButton.addButton(self.sharedLibRadio, Project.Target.SharedLibrary)
      targetButton.addButton(self.staticLibRadio, Project.Target.StaticLibrary)

      componentsButton = QButtonGroup(self)
      componentsButton.setExclusive(False)
      componentsButton.idToggled.connect(self.componentsChanged)

      componentsButton.addButton(self.compNetworkCheck, Project.Components.Network)

      featuresButton = QButtonGroup(self)
      featuresButton.setExclusive(False)
      featuresButton.idToggled.connect(self.featuresChanged)

      featuresButton.addButton(self.precompiledCheck, Project.Features.PreCompiledHeader)
      featuresButton.addButton(self.iconCheck, Project.Features.AppIcon)
      featuresButton.addButton(self.mainCheck, Project.Features.CreateMain)
      featuresButton.addButton(self.gitCheck, Project.Features.CreateGit)

      self.startButton.clicked.connect(self.create)  # can not call create of project directly

   def create(self):

      self.logEdit.clear()
      self._create()
