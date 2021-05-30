# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(987, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.recipients_label = QtWidgets.QLabel(self.centralwidget)
        self.recipients_label.setFrameShape(QtWidgets.QFrame.Box)
        self.recipients_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.recipients_label.setAlignment(QtCore.Qt.AlignCenter)
        self.recipients_label.setObjectName("recipients_label")
        self.verticalLayout.addWidget(self.recipients_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_name_add = QtWidgets.QLineEdit(self.centralwidget)
        self.input_name_add.setObjectName("input_name_add")
        self.horizontalLayout.addWidget(self.input_name_add)
        self.add_name = QtWidgets.QPushButton(self.centralwidget)
        self.add_name.setObjectName("add_name")
        self.horizontalLayout.addWidget(self.add_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.recipients_list = QtWidgets.QListWidget(self.centralwidget)
        self.recipients_list.setObjectName("recipients_list")
        self.verticalLayout.addWidget(self.recipients_list)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.recipient = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.recipient.setFont(font)
        self.recipient.setStyleSheet("")
        self.recipient.setFrameShape(QtWidgets.QFrame.Box)
        self.recipient.setText("")
        self.recipient.setObjectName("recipient")
        self.verticalLayout_2.addWidget(self.recipient)
        self.messages = QtWidgets.QTextBrowser(self.centralwidget)
        self.messages.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.messages.setObjectName("messages")
        self.verticalLayout_2.addWidget(self.messages)
        self.input_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_text.setEnabled(True)
        self.input_text.setMaximumSize(QtCore.QSize(16777215, 100))
        self.input_text.setObjectName("input_text")
        self.verticalLayout_2.addWidget(self.input_text)
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setObjectName("send")
        self.verticalLayout_2.addWidget(self.send)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 987, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QChat"))
        self.recipients_label.setText(_translate("MainWindow", "Contacts"))
        self.add_name.setText(_translate("MainWindow", "Add contact"))
        self.messages.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.send.setText(_translate("MainWindow", "Send"))

