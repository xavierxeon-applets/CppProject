# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QGridLayout,
    QGroupBox, QHeaderView, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QTextEdit, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(683, 699)
        self.gridLayout = QGridLayout(MainWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.typeGroup = QGroupBox(MainWidget)
        self.typeGroup.setObjectName(u"typeGroup")
        self.typeGroup.setFlat(True)
        self.verticalLayout = QVBoxLayout(self.typeGroup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widgetsRadio = QRadioButton(self.typeGroup)
        self.widgetsRadio.setObjectName(u"widgetsRadio")
        self.widgetsRadio.setChecked(True)

        self.verticalLayout.addWidget(self.widgetsRadio)

        self.qmlRadio = QRadioButton(self.typeGroup)
        self.qmlRadio.setObjectName(u"qmlRadio")

        self.verticalLayout.addWidget(self.qmlRadio)

        self.cppRadio = QRadioButton(self.typeGroup)
        self.cppRadio.setObjectName(u"cppRadio")

        self.verticalLayout.addWidget(self.cppRadio)


        self.gridLayout.addWidget(self.typeGroup, 0, 0, 2, 1)

        self.operationGroup = QGroupBox(MainWidget)
        self.operationGroup.setObjectName(u"operationGroup")
        self.operationGroup.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.operationGroup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.startButton = QPushButton(self.operationGroup)
        self.startButton.setObjectName(u"startButton")

        self.verticalLayout_3.addWidget(self.startButton)


        self.gridLayout.addWidget(self.operationGroup, 0, 1, 1, 1)

        self.overwriteGroup = QGroupBox(MainWidget)
        self.overwriteGroup.setObjectName(u"overwriteGroup")
        self.overwriteGroup.setFlat(True)
        self.verticalLayout_7 = QVBoxLayout(self.overwriteGroup)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.overwriteTree = QTreeView(self.overwriteGroup)
        self.overwriteTree.setObjectName(u"overwriteTree")
        self.overwriteTree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.overwriteTree.setRootIsDecorated(False)
        self.overwriteTree.setHeaderHidden(True)

        self.verticalLayout_7.addWidget(self.overwriteTree)


        self.gridLayout.addWidget(self.overwriteGroup, 1, 1, 3, 1)

        self.targetGroup = QGroupBox(MainWidget)
        self.targetGroup.setObjectName(u"targetGroup")
        self.targetGroup.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.targetGroup)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.appRadio = QRadioButton(self.targetGroup)
        self.appRadio.setObjectName(u"appRadio")
        self.appRadio.setChecked(True)

        self.verticalLayout_2.addWidget(self.appRadio)

        self.sharedLibRadio = QRadioButton(self.targetGroup)
        self.sharedLibRadio.setObjectName(u"sharedLibRadio")

        self.verticalLayout_2.addWidget(self.sharedLibRadio)

        self.staticLibRadio = QRadioButton(self.targetGroup)
        self.staticLibRadio.setObjectName(u"staticLibRadio")

        self.verticalLayout_2.addWidget(self.staticLibRadio)


        self.gridLayout.addWidget(self.targetGroup, 2, 0, 1, 1)

        self.componentGroup = QGroupBox(MainWidget)
        self.componentGroup.setObjectName(u"componentGroup")
        self.componentGroup.setFlat(True)
        self.verticalLayout_4 = QVBoxLayout(self.componentGroup)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.compNetworkCheck = QCheckBox(self.componentGroup)
        self.compNetworkCheck.setObjectName(u"compNetworkCheck")

        self.verticalLayout_4.addWidget(self.compNetworkCheck)


        self.gridLayout.addWidget(self.componentGroup, 3, 0, 1, 1)

        self.featureGroup = QGroupBox(MainWidget)
        self.featureGroup.setObjectName(u"featureGroup")
        self.featureGroup.setFlat(True)
        self.verticalLayout_5 = QVBoxLayout(self.featureGroup)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.precompiledCheck = QCheckBox(self.featureGroup)
        self.precompiledCheck.setObjectName(u"precompiledCheck")
        self.precompiledCheck.setChecked(True)

        self.verticalLayout_5.addWidget(self.precompiledCheck)

        self.iconCheck = QCheckBox(self.featureGroup)
        self.iconCheck.setObjectName(u"iconCheck")

        self.verticalLayout_5.addWidget(self.iconCheck)

        self.mainCheck = QCheckBox(self.featureGroup)
        self.mainCheck.setObjectName(u"mainCheck")
        self.mainCheck.setChecked(True)

        self.verticalLayout_5.addWidget(self.mainCheck)

        self.gitCheck = QCheckBox(self.featureGroup)
        self.gitCheck.setObjectName(u"gitCheck")

        self.verticalLayout_5.addWidget(self.gitCheck)

        self.qmlDummyCheck = QCheckBox(self.featureGroup)
        self.qmlDummyCheck.setObjectName(u"qmlDummyCheck")

        self.verticalLayout_5.addWidget(self.qmlDummyCheck)


        self.gridLayout.addWidget(self.featureGroup, 4, 0, 1, 1)

        self.logGroup = QGroupBox(MainWidget)
        self.logGroup.setObjectName(u"logGroup")
        self.logGroup.setFlat(True)
        self.verticalLayout_6 = QVBoxLayout(self.logGroup)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.logEdit = QTextEdit(self.logGroup)
        self.logEdit.setObjectName(u"logEdit")
        self.logEdit.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.logEdit)


        self.gridLayout.addWidget(self.logGroup, 4, 1, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Create Project", None))
        self.typeGroup.setTitle(QCoreApplication.translate("MainWidget", u"Type", None))
        self.widgetsRadio.setText(QCoreApplication.translate("MainWidget", u"Widgets", None))
        self.qmlRadio.setText(QCoreApplication.translate("MainWidget", u"QML", None))
        self.cppRadio.setText(QCoreApplication.translate("MainWidget", u"C++", None))
        self.operationGroup.setTitle(QCoreApplication.translate("MainWidget", u"Operation", None))
        self.startButton.setText(QCoreApplication.translate("MainWidget", u"Create Project", None))
        self.overwriteGroup.setTitle(QCoreApplication.translate("MainWidget", u"Overwrite", None))
        self.targetGroup.setTitle(QCoreApplication.translate("MainWidget", u"Target", None))
        self.appRadio.setText(QCoreApplication.translate("MainWidget", u"Application", None))
        self.sharedLibRadio.setText(QCoreApplication.translate("MainWidget", u"Shared Library", None))
        self.staticLibRadio.setText(QCoreApplication.translate("MainWidget", u"Static Library", None))
        self.componentGroup.setTitle(QCoreApplication.translate("MainWidget", u"Qt Components", None))
        self.compNetworkCheck.setText(QCoreApplication.translate("MainWidget", u"Network", None))
        self.featureGroup.setTitle(QCoreApplication.translate("MainWidget", u"Features", None))
        self.precompiledCheck.setText(QCoreApplication.translate("MainWidget", u"pre compiled header", None))
        self.iconCheck.setText(QCoreApplication.translate("MainWidget", u"app icon", None))
        self.mainCheck.setText(QCoreApplication.translate("MainWidget", u"create main", None))
        self.gitCheck.setText(QCoreApplication.translate("MainWidget", u"create git", None))
        self.qmlDummyCheck.setText(QCoreApplication.translate("MainWidget", u"create QmlType", None))
        self.logGroup.setTitle(QCoreApplication.translate("MainWidget", u"Log", None))
    # retranslateUi

