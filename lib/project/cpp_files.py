#

from ..file_writer import FileWriter
from .defs import *


class CppFiles:

   def __init__(self, project, files_model):

      self.project = project
      self.files_model = files_model

      self.update()

   def update(self):

      self.files_model.registerFile('MainWidget.h', self.project._type == Type.Widgets)
      self.files_model.registerFile('MainWidget.cpp', self.project._type == Type.Widgets)

      self.files_model.registerFile('main.cpp', self.project._type != Type.Widgets)

   def generate(self):

      if not self.project._features & Features.CreateMain:
         return

      if self.project._type == Type.Cpp:
         self.writeCppMain()
      elif self.project._type == Type.QML:
         self.writeQmlMain()
      else:
         self.writeWidgetsMainHeader()
         self.writeWidgetsMainSource()

   def writeCppMain(self):

      self.files_model.maybeClean('main.cpp')
      with FileWriter('main.cpp') as line:

         line('//')
         line()
         line('int main(int argc, char** argv)')
         line('{')
         line('   return 0;')
         line('}')
         line()

   def writeQmlMain(self):

      self.files_model.maybeClean('main.cpp')
      with FileWriter('main.cpp') as line:

         line('// main function')
         line()
         line('#include <QGuiApplication>')
         line()
         line('#include <XXQmlView.h>')
         line()
         line('int main(int argc, char** argv)')
         line('{')
         line('   QGuiApplication app(argc, argv);')
         line()
         line('   XX::QmlView view;')
         line('   view.setSource(QUrl("qrc:/Gui/MainWindow.qml"));')
         line(f'   view.setTitle("{self.project.name}");')
         line('   view.show();')
         line()
         line('   return app.exec();')
         line('}')

   def writeWidgetsMainHeader(self):

      self.files_model.maybeClean('MainWidget.h')
      with FileWriter('MainWidget.h') as line:

         line('#ifndef MainWidgetH')
         line('#define MainWidgetH')
         line()
         line('#include <QWidget>')
         line()
         line('class MainWidget : public QWidget')
         line('{')
         line('   Q_OBJECT')
         line('public:')
         line('   MainWidget();')
         line('};')
         line()
         line('  # endif // NOT MainWidgetH')
         line()

   def writeWidgetsMainSource(self):

      self.files_model.maybeClean('MainWidget.cpp')
      with FileWriter('MainWidget.cpp') as line:

         line('#include "MainWidget.h"')
         line()
         line('#include <QApplication>')
         line()
         line('MainWidget::MainWidget()')
         line('   : QWidget(nullptr)')
         line('{')
         line('}')
         line()
         line('// main function')
         line()
         line('int main(int argc, char** argv)')
         line('{')
         line('   QApplication app(argc, argv);')
         line()
         line('   MainWidget mw;')
         line('   mw.show();')
         line()
         line('   return app.exec();')
         line('}')
         line()
