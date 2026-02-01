#

import os
from ..file_writer import FileWriter
from .defs import *


class QmlFiles:

   def __init__(self, project, files_model):

      self.project = project
      self.files_model = files_model

      self.update()

   def update(self):

      self.files_model.registerFile('Gui/MainWindow.qml', self.project._type == Type.QML)
      self.files_model.registerFile('QmlTypes/Dummy.h', self.project._features & Features.CreateQmlType)
      self.files_model.registerFile('QmlTypes/Dummy.cpp', self.project._features & Features.CreateQmlType)

   def generate(self):

      if self.project._type == Type.QML:
         os.makedirs('Gui', exist_ok=True)
         self.writeMainWindow()

      if self.project._features & Features.CreateQmlType:
         os.makedirs('QmlTypes', exist_ok=True)
         self.writeQmlTypeHeader()
         self.writeQmlTypeSource()

   def writeMainWindow(self):

      self.files_model.maybeClean('Gui/MainWindow.qml')
      with FileWriter('Gui/MainWindow.qml') as line:
         line('import QtQuick')
         line('import QtQuick.Layouts')
         line('')
         line('Window {')
         line('   id: window')
         line('')
         line('   visible: true')
         line(f'   title: "{self.project.name}"')
         line('}')
         line()

   def writeQmlTypeHeader(self):

      self.files_model.maybeClean('QmlTypes/Dummy.h')
      with FileWriter('QmlTypes/Dummy.h') as line:
         line('#ifndef DummyH')
         line('#define DummyH')
         line('')
         line('#include <QQuickItem>')
         line('#include <QQmlEngine>')
         line('')
         line('class Dummy : public QQuickItem')
         line('{')
         line('   Q_OBJECT')
         line('   QML_NAMED_ELEMENT(Dummy)')
         line('')
         line('public:')
         line('   Dummy(QQuickItem* parent);')
         line('};')
         line('')
         line('#endif // NOT DummyH')
         line()

   def writeQmlTypeSource(self):

      self.files_model.maybeClean('QmlTypes/Dummy.cpp')
      with FileWriter('QmlTypes/Dummy.cpp') as line:
         line('#include "Dummy.h"')
         line('')
         line('Dummy::Dummy(QQuickItem* parent)')
         line('   : QQuickItem(parent)')
         line('{')
         line('}')
         line()
