import sys
import win32api
import traceback

from shuncom_ui.window_son.version_information_ui.tool_version_information import Ui_tool_version_information
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui

class version_info(QMainWindow, Ui_tool_version_information):
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(version_info, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()

    def initUI(self):
        '''界面控件绑定'''

        self.pushButton.clicked.connect(self.Dowload_instructions)
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            #self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint )# 窗口置顶
            self.add_shadow(self.pushButton)
        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.m_flag = True
    #         self.m_Position = event.globalPos() - self.pos()
    #         event.accept()
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     if Qt.LeftButton and self.m_flag:
    #         self.move(QMouseEvent.globalPos() - self.m_Position)
    #         QMouseEvent.accept()
    #
    # def mouseRelease(self, QMouseEvent):
    #     self.m_flag = False
    #     self.setCursor(QCursor(Qt.ArrowCursor))

    ############################################自写函数#########################################
    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)

    def add_shadow_white(self, control, value=3):
        '''给控件添加白色阴影'''
        try:
            effect_shadow = QGraphicsDropShadowEffect()
            effect_shadow.setOffset(0, 0)  # 设置偏移量
            effect_shadow.setBlurRadius(value)  # 设置阴影范围
            effect_shadow.setColor(QtCore.Qt.white)  # 设置阴影颜色为白色
            control.setGraphicsEffect(effect_shadow)  # 将阴影加入到控件
        except Exception as e:
            print(traceback.print_exc())


    def add_shadow(self, pushbutton, value=4):
        '''给按钮添加阴影效果'''
        try:
            effect_shadow = QGraphicsDropShadowEffect()
            effect_shadow.setOffset(0, 0)#设置偏移量
            effect_shadow.setBlurRadius(value)#设置阴影范围
            effect_shadow.setColor(QtCore.Qt.gray)#设置阴影颜色为灰色
            pushbutton.setGraphicsEffect(effect_shadow)#将阴影加入到按钮
        except Exception as e:
            print(traceback.print_exc())

    def Dowload_instructions(self):
        '''下载使用说明书'''
        try:
            # self.signal_Popup_Qtime_QtCore.emit('提示', '暂无操作手册！')
            win32api.ShellExecute(None, 'open', '.\HelpBook\网关局域网调试工具帮助手册.pdf', None, None, 1)
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def signal_Popup(self, newtypes, news):
        try:
            if newtypes == '警告':
                QMessageBox.warning(self, '警告', news)
            if newtypes == '提示':
                QMessageBox.information(self, '提示', news)
            if newtypes == '危险':
                QMessageBox.ctitical(self, '危险', news)
            if newtypes == '问答':
                QMessageBox.question(self, '问答', news)
            if newtypes == '关于':
                QMessageBox.about(self, '关于', news)
        except Exception as e:
            print(traceback.print_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = version_info()
    myWin.show()
    sys.exit(app.exec_())