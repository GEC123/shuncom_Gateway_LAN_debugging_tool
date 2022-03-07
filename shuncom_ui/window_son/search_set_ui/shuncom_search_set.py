import traceback
import sys
from shuncom_ui.window_son.search_set_ui.tool_search_set import Ui_tool_search_set
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect, QMessageBox



class search_set_MainWindow(QtWidgets.QMainWindow, Ui_tool_search_set):
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self):
        super(search_set_MainWindow, self).__init__()
        self.setupUi(self)
        self.init()
        self.selectstate = 0  # 选择状态
        self.SET_UI_QSS()
        self.IP_data = {}

    def init(self):
        '''信号槽绑定'''
        self.pushButton.clicked.connect(self.Enter_fun)#确定按钮
        self.pushButton_2.clicked.connect(self.close)#取消按钮

        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            #self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)# 窗口置顶
            self.add_shadow(self.pushButton_2)
            self.add_shadow(self.spinBox_1)
            self.add_shadow(self.spinBox_2)
            self.add_shadow(self.spinBox_3)
            self.add_shadow(self.spinBox_4)
            self.add_shadow(self.spinBox_5)
            self.add_shadow(self.spinBox_6)
            self.add_shadow(self.spinBox_7)
            self.add_shadow(self.spinBox_8)
        except Exception as e:
            print(traceback.print_exc())
    ##########################################官方函数重写#########################################
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


    def Enter_fun(self):
        try:

            if self.radioButton.isChecked() == True:#本网段
                self.IP_data['type'] = 'local'

            if self.radioButton_2.isChecked() ==  True:#指定其他网段
                if int(self.spinBox_2.text()) > int(self.spinBox_6.text()) or int(self.spinBox_1.text()) > int(
                        self.spinBox_5.text()):
                    QMessageBox.information(self, '提示', '数据设置出错!')
                    return
                self.IP_data['type'] = 'other'
                self.IP_data['net1_part1'] = self.spinBox_1.text()
                self.IP_data['net1_part2'] = self.spinBox_2.text()
                self.IP_data['net1_part3'] = self.spinBox_3.text()
                self.IP_data['net1_part4'] = self.spinBox_4.text()

                self.IP_data['net2_part1'] = self.spinBox_5.text()
                self.IP_data['net2_part2'] = self.spinBox_6.text()
                self.IP_data['net2_part3'] = self.spinBox_7.text()
                self.IP_data['net2_part4'] = self.spinBox_8.text()
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def Init_Window_Data(self, search_set_data):
        '''初始化界面数据'''
        try:
            if len(search_set_data) == 0:
                return
            self.IP_data = search_set_data
            if self.IP_data['type'] == 'local':
                self.radioButton.setChecked(True)
                self.radioButton_2.setChecked(False)
                self.groupBox_4.setEnabled(False)
                self.groupBox_6.setEnabled(False)
            else:
                self.radioButton.setChecked(False)
                self.radioButton_2.setChecked(True)
                self.groupBox_4.setEnabled(True)
                self.groupBox_6.setEnabled(True)
                self.spinBox_4.setValue(int(self.IP_data['net1_part4']))
                self.spinBox_3.setValue(int(self.IP_data['net1_part3']))
                self.spinBox_2.setValue(int(self.IP_data['net1_part2']))
                self.spinBox_1.setValue(int(self.IP_data['net1_part1']))

                self.spinBox_8.setValue(int(self.IP_data['net2_part4']))
                self.spinBox_7.setValue(int(self.IP_data['net2_part3']))
                self.spinBox_6.setValue(int(self.IP_data['net2_part2']))
                self.spinBox_5.setValue(int(self.IP_data['net2_part1']))
            print('搜索网段设置页面初始化完成')
        except Exception as e:
            print(traceback.print_exc())

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
            effect_shadow.setOffset(0, 0)  # 设置偏移量
            effect_shadow.setBlurRadius(value)  # 设置阴影范围
            effect_shadow.setColor(QtCore.Qt.gray)  # 设置阴影颜色为灰色
            pushbutton.setGraphicsEffect(effect_shadow)  # 将阴影加入到按钮
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
    window = search_set_MainWindow()
    window.show()
    QApplication.processEvents()
    sys.exit(app.exec_())