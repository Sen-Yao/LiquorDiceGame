# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ldg.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 461)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Label1 = QLabel(Form)
        self.Label1.setObjectName(u"Label1")

        self.verticalLayout.addWidget(self.Label1)

        self.PlayerList = QListWidget(Form)
        self.PlayerList.setObjectName(u"PlayerList")

        self.verticalLayout.addWidget(self.PlayerList)

        self.DeletePlayerButton = QPushButton(Form)
        self.DeletePlayerButton.setObjectName(u"DeletePlayerButton")

        self.verticalLayout.addWidget(self.DeletePlayerButton)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Label2 = QLabel(self.widget)
        self.Label2.setObjectName(u"Label2")

        self.horizontalLayout.addWidget(self.Label2)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")

        self.horizontalLayout.addWidget(self.widget_2)

        self.MaxPlayerEdit = QLineEdit(self.widget)
        self.MaxPlayerEdit.setObjectName(u"MaxPlayerEdit")

        self.horizontalLayout.addWidget(self.MaxPlayerEdit)


        self.verticalLayout.addWidget(self.widget)

        self.widget_5 = QWidget(Form)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")

        self.horizontalLayout_4.addWidget(self.widget_6)

        self.MaxPlayRoundEdit = QLineEdit(self.widget_5)
        self.MaxPlayRoundEdit.setObjectName(u"MaxPlayRoundEdit")

        self.horizontalLayout_4.addWidget(self.MaxPlayRoundEdit)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Label3 = QLabel(self.widget_3)
        self.Label3.setObjectName(u"Label3")

        self.horizontalLayout_2.addWidget(self.Label3)

        self.AllowZhai = QRadioButton(self.widget_3)
        self.AllowZhai.setObjectName(u"AllowZhai")

        self.horizontalLayout_2.addWidget(self.AllowZhai)

        self.DisallowZhai = QRadioButton(self.widget_3)
        self.DisallowZhai.setObjectName(u"DisallowZhai")

        self.horizontalLayout_2.addWidget(self.DisallowZhai)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(Form)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Label4 = QLabel(self.widget_4)
        self.Label4.setObjectName(u"Label4")

        self.horizontalLayout_3.addWidget(self.Label4)

        self.AllowJump = QRadioButton(self.widget_4)
        self.AllowJump.setObjectName(u"AllowJump")

        self.horizontalLayout_3.addWidget(self.AllowJump)

        self.DisallowJump = QRadioButton(self.widget_4)
        self.DisallowJump.setObjectName(u"DisallowJump")

        self.horizontalLayout_3.addWidget(self.DisallowJump)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_7 = QWidget(Form)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.CloseButton = QPushButton(self.widget_7)
        self.CloseButton.setObjectName(u"CloseButton")

        self.horizontalLayout_5.addWidget(self.CloseButton)

        self.widget_8 = QWidget(self.widget_7)
        self.widget_8.setObjectName(u"widget_8")

        self.horizontalLayout_5.addWidget(self.widget_8)

        self.StartButton = QPushButton(self.widget_7)
        self.StartButton.setObjectName(u"StartButton")

        self.horizontalLayout_5.addWidget(self.StartButton)


        self.verticalLayout.addWidget(self.widget_7)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u670d\u52a1\u5668", None))
        self.Label1.setText(QCoreApplication.translate("Form", u"\u73a9\u5bb6\u5217\u8868", None))
        self.DeletePlayerButton.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u73a9\u5bb6", None))
        self.Label2.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u73a9\u5bb6\u6570", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u6e38\u73a9\u5c40\u6570", None))
        self.Label3.setText(QCoreApplication.translate("Form", u"\u658b\u98de\u89c4\u5219", None))
        self.AllowZhai.setText(QCoreApplication.translate("Form", u"\u5141\u8bb8", None))
        self.DisallowZhai.setText(QCoreApplication.translate("Form", u"\u4e0d\u5141\u8bb8", None))
        self.Label4.setText(QCoreApplication.translate("Form", u"\u8df3\u5f00\u89c4\u5219", None))
        self.AllowJump.setText(QCoreApplication.translate("Form", u"\u5141\u8bb8", None))
        self.DisallowJump.setText(QCoreApplication.translate("Form", u"\u4e0d\u5141\u8bb8", None))
        self.CloseButton.setText(QCoreApplication.translate("Form", u"\u5173\u95ed\u670d\u52a1\u5668", None))
        self.StartButton.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u6e38\u620f", None))
    # retranslateUi

