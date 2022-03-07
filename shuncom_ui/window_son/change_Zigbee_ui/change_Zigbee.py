import sys
import traceback
from shuncom_ui.window_son.change_Zigbee_ui.tool_change import Ui_tool_change
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtGui
from shuncom_module.shuncom_fun import *

class change_Zigbee(QMainWindow, Ui_tool_change):
    zigbee_window_exit_signal = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(change_Zigbee, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.lastip = None  # 上一次选择的设备IP
        self.WINDOW_DATA = {}  # 保留界面数据
        self.device_data = {}  # 被选中的设备信息

    def initUI(self):
        '''界面控件绑定'''
        self.pushButton_2.clicked.connect(self.Exit_window_func)
        self.pushButton.clicked.connect(self.SAVE_DATA_WINDOW)
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)# 窗口置顶
            self.add_shadow(self.comboBox)
            self.add_shadow(self.pushButton_2)
            self.add_shadow(self.lineEdit)

        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.zigbee_window_exit_signal.emit()

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

    def Exit_window_func(self):
        '''退出界面操作'''
        try:
            self.selectstate = 0
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def pid_ip_formatc_heck(self, pid_id):
        '''频点IP格式校验'''
        try:
            if len(pid_id) != 4:
                return False
            pid_id_list = list(pid_id)
            pid_id_4 = pid_id_list[0]
            pid_id_3 = pid_id_list[1]
            pid_id_2 = pid_id_list[2]
            pid_id_1 = pid_id_list[3]
            if pid_id_4 > 'F' or pid_id_4 < '0':
                return False
            if pid_id_3 > 'F' or pid_id_4 < '0':
                return False
            if pid_id_2 > 'F' or pid_id_4 < '0':
                return False
            if pid_id_1 > 'F' or pid_id_4 < '0':
                return False
        except Exception as e:
            print(traceback.print_exc())


    def SAVE_DATA_WINDOW(self):
        '''保留界面数据'''
        try:
            if len(self.device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('警告', '未勾选设备!')
                return
            channel_Hz = self.comboBox.currentText()
            channel = channel_Hz.split('(')[0]
            pid_id = self.lineEdit.text()

            if self.pid_ip_formatc_heck(pid_id) == False:
                self.signal_Popup_Qtime_QtCore.emit('提示', '数据格式错误!')
                return
            self.WINDOW_DATA['频点'] = int(hex2dec(channel))
            self.WINDOW_DATA['频点ID'] = int(hex2dec(pid_id))

            print(self.WINDOW_DATA)
            self.selectstate = 1
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def window_updata(self):
        try:
            mac_list = list(self.device_data.keys())
            if mac_list != []:
                ip = self.device_data[mac_list[0]]['ipaddr']
            self.label_4.setText(str(len(mac_list)))
            if len(mac_list) < 1 or len(mac_list) > 1:
                self.WindowShowModule = 'MORE'
                self.comboBox.setCurrentIndex(0)
                self.lineEdit.setText('')
            else:
                if self.lastip == None:
                    self.lastip = ip
                elif self.lastip == ip:
                    return
                self.comboBox.setCurrentIndex(self.device_data[mac_list[0]]['channel'])
                self.lineEdit.setText(D_to_H(self.device_data[mac_list[0]]['pan_id']))
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
    myWin = change_Zigbee()
    myWin.show()
    sys.exit(app.exec_())