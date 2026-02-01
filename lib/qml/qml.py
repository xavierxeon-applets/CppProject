#

from ..file_writer import FileWriter

def createQml(fileName):

   if not fileName.endswith('.qml'):
      fileName += '.qml'

   with FileWriter(fileName) as line:
      line('import QtQuick')
      line('import QtQuick.Layouts')
      line('import QtQuick.Controls')
      line()
      line('Rectangle {')
      line('   width: 200')
      line('   height: 200')
      line('   color: "lightgray"')
      line()
      line('   Text {')
      line('      text: "Hello, QML!"')
      line('      anchors.centerIn: parent')
      line('   }')
      line('}')