# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool_Administrator.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tool_Administrator(object):
    def setupUi(self, tool_Administrator):
        tool_Administrator.setObjectName("tool_Administrator")
        tool_Administrator.resize(600, 260)
        tool_Administrator.setMinimumSize(QtCore.QSize(600, 260))
        tool_Administrator.setMaximumSize(QtCore.QSize(600, 260))
        tool_Administrator.setStyleSheet("QMainWindow\n"
"{\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(tool_Administrator)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 30, 601, 181))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(100, 60, 374, 56))
        self.groupBox_2.setStyleSheet("border : none;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setMinimumSize(QtCore.QSize(260, 32))
        self.lineEdit.setMaximumSize(QtCore.QSize(260, 32))
        self.lineEdit.setStyleSheet("border : none;")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setStyleSheet("color: rgb(50, 50, 51);")
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        tool_Administrator.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(tool_Administrator)
        self.statusbar.setObjectName("statusbar")
        tool_Administrator.setStatusBar(self.statusbar)

        self.retranslateUi(tool_Administrator)
        QtCore.QMetaObject.connectSlotsByName(tool_Administrator)

    def retranslateUi(self, tool_Administrator):
        _translate = QtCore.QCoreApplication.translate
        tool_Administrator.setWindowTitle(_translate("tool_Administrator", "管理员登录"))
        self.label.setText(_translate("tool_Administrator", "管理员密码:"))
