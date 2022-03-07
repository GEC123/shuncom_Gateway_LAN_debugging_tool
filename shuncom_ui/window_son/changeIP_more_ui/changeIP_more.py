import sys
import traceback
from shuncom_ui.window_son.changeIP_more_ui.tool_changeIP_more import Ui_tool_changeIP_more
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui
class changeIP_more(QMainWindow, Ui_tool_changeIP_more):
    ipmore_window_exit_signal = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(changeIP_more, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.IPDATA = {}#保留界面数据
        self.lastip = None  # 上一次操作的IP
        self.device_data = {}#被选中的设备信息


    def initUI(self):
        '''界面控件绑定'''
        self.pushButton_2.clicked.connect(self.Exit_window_func)
        self.pushButton.clicked.connect(self.SAVE_DATA_WINDOW)
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            #self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)# 窗口置顶
            self.add_shadow(self.pushButton_2)
            self.add_shadow(self.spinBox)
            self.add_shadow(self.spinBox_2)
            self.add_shadow(self.spinBox_3)
            self.add_shadow(self.spinBox_4)
            self.add_shadow(self.spinBox_5)
            self.add_shadow(self.spinBox_6)
            self.add_shadow(self.spinBox_7)
            self.add_shadow(self.spinBox_8)
            self.add_shadow(self.spinBox_9)
            self.add_shadow(self.spinBox_10)
            self.add_shadow(self.spinBox_11)
            self.add_shadow(self.spinBox_12)
            self.add_shadow(self.spinBox_13)
            self.add_shadow(self.spinBox_14)
            self.add_shadow(self.spinBox_15)
            self.add_shadow(self.spinBox_16)
            self.add_shadow(self.spinBox_17)
            self.add_shadow(self.spinBox_18)
            self.add_shadow(self.spinBox_19)
            self.add_shadow(self.spinBox_20)
            self.add_shadow(self.spinBox_21)
            self.add_shadow(self.spinBox_22)
            self.add_shadow(self.spinBox_23)
            self.add_shadow(self.spinBox_24)
        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ipmore_window_exit_signal.emit()

    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)


    ############################################自写函数#########################################



    def Exit_window_func(self):
        '''退出界面操作'''
        try:
            self.selectstate = 0
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def SAVE_DATA_WINDOW(self):
        '''保留界面数据'''
        try:
            if len(self.device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('警告', '未勾选设备!')
                return
            # 1、数据检查
            if (self.spinBox_4.text() == self.spinBox_8.text() and self.spinBox_3.text() == self.spinBox_7.text()
            and self.spinBox_2.text() <= self.spinBox_6.text()):  # 网段检查
                if (int(self.spinBox_5.text()) - int(self.spinBox.text())) + 1 >= len(self.device_data):  # 范围检查
                    pass
                else:
                    self.signal_Popup_Qtime_QtCore.emit('提示', '范围过小!')
                    return
            else:
                self.signal_Popup_Qtime_QtCore.emit('提示', '网段错误!')
                return
            if self.netcard_check() == False:
                return

            # 2、数据保存
            self.IPDATA.clear()
            if self.radioButton.isChecked() == True:
                self.IPDATA['proto'] = 'static'
                self.IPDATA['start_ip'] = [self.spinBox_4.text(), self.spinBox_3.text(), self.spinBox_2.text(), self.spinBox.text()]
                self.IPDATA['end_ip'] = [self.spinBox_8.text(), self.spinBox_7.text(), self.spinBox_6.text(), self.spinBox_5.text()]
                self.IPDATA['netmask'] = '.'.join([self.spinBox_12.text(), self.spinBox_11.text(), self.spinBox_10.text(), self.spinBox_9.text()])
                self.IPDATA['gateway'] = '.'.join([self.spinBox_16.text(), self.spinBox_15.text(), self.spinBox_14.text(), self.spinBox_13.text()])
                self.IPDATA['dns1'] = '.'.join([self.spinBox_20.text(), self.spinBox_19.text(), self.spinBox_18.text(), self.spinBox_17.text()])
                self.IPDATA['dns2'] = '.'.join([self.spinBox_24.text(), self.spinBox_23.text(), self.spinBox_22.text(), self.spinBox_21.text()])
            else:
                self.IPDATA['proto'] = 'dhcp'
            print(self.IPDATA)
            self.selectstate = 1
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def netcard_check(self):
        '''网段检查'''
        try:
            key_list = list(self.device_data.keys())
            if self.radioButton.isChecked() == True:
                network_data = []
                for card in range(int(self.spinBox_2.text()), int(self.spinBox_6.text()) + 1):
                    for last in range(int(self.spinBox.text()), int(self.spinBox_5.text()) + 1):
                        ip = '.'.join([self.spinBox_4.text(), self.spinBox_3.text(), str(card), str(last)])
                        network_data.append({"ipaddr": ip})

                for i in range(len(key_list)):

                    mac = key_list[i]
                    ip = self.device_data[mac]['ipaddr']
                    oldcard = ip.split('.')[2]
                    newcard = network_data[i]['ipaddr'].split('.')[2]
                    # print(oldcard, newcard)
                    if oldcard != newcard:
                        result = QMessageBox.information(self, '提示', '修改设备的网段将会导致设备不可用，是否继续？',
                                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if result == QMessageBox.Yes:
                            return True
                        else:
                            return False
        except Exception as e:
            print(traceback.print_exc())

    def window_updata(self):
        try:
            device_num = len(self.device_data)
            self.label_23.setText(str(device_num))
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
            effect_shadow.setOffset(0, 0)#设置偏移量
            effect_shadow.setBlurRadius(value)#设置阴影范围
            effect_shadow.setColor(QtCore.Qt.gray)#设置阴影颜色为灰色
            pushbutton.setGraphicsEffect(effect_shadow)#将阴影加入到按钮
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
    myWin = changeIP_more()
    myWin.show()
    sys.exit(app.exec_())