import sys
import traceback
from shuncom_ui.window_son.changeIP_single_ui.tool_changeIP_single import Ui_tool_changeIP_single
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore

class changeIP_single(QMainWindow, Ui_tool_changeIP_single):
    ipsingle_window_exit_signal = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(changeIP_single, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.IPDATA = {}  # 保留界面数据
        self.lastip = None  # 上一次操作的IP
        self.device_data = {}#被选中的设备信息

    def initUI(self):
        '''界面控件绑定'''
        self.pushButton_2.clicked.connect(self.Exit_window_func)
        self.pushButton.clicked.connect(self.Enterevent)
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

        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################
    def closeEvent(self, event):
        self.CLEAR_DATA_WINDOW()
        self.ipsingle_window_exit_signal.emit()


    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)

    ############################################自写函数#########################################
    def Exit_window_func(self):
        try:
            self.selectstate = 0
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def Enterevent(self):
        try:
            if len(self.device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未勾选设备')
                return
            else:
                self.selectstate = 1
                self.SAVE_DATA_WINDOW()

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

    def SAVE_DATA_WINDOW(self):
        '''保留界面数据'''
        try:
            self.IPDATA.clear()
            if self.radioButton.isChecked() == True:
                self.IPDATA['proto'] = 'static'
                self.IPDATA['ipaddr'] = '.'.join([self.spinBox_4.text(), self.spinBox_3.text(), self.spinBox_2.text(), self.spinBox.text()])
                self.IPDATA['netmask'] = '.'.join([self.spinBox_8.text(), self.spinBox_7.text(), self.spinBox_6.text(), self.spinBox_5.text()])
                self.IPDATA['gateway'] = '.'.join([self.spinBox_12.text(), self.spinBox_11.text(), self.spinBox_10.text(), self.spinBox_9.text()])
                self.IPDATA['dns1'] = '.'.join([self.spinBox_16.text(), self.spinBox_15.text(), self.spinBox_14.text(), self.spinBox_13.text()])
                self.IPDATA['dns2'] = '.'.join([self.spinBox_20.text(), self.spinBox_19.text(), self.spinBox_18.text(), self.spinBox_17.text()])
            else:
                self.IPDATA['proto'] = 'dhcp'
            print(self.IPDATA)
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def WindowDateInit(self):
        '''界面数据初始化'''
        try:
            if len(self.device_data) == 0:   # 未选择设备
                self.label_23.setText('0')
                return
            else:
                self.label_23.setText('1')
                mac = list(self.device_data)[0]
                ip = self.device_data[mac]['ipaddr']
                if self.device_data[mac]['proto'] == 'dhcp':  # 动态连接方式
                    self.radioButton_2.setChecked(True)
                    self.radioButton.setChecked(False)
                    self.groupBox_4.setEnabled(False)
                    self.groupBox_6.setEnabled(False)
                    self.groupBox_8.setEnabled(False)
                    self.groupBox_10.setEnabled(False)
                    self.groupBox_12.setEnabled(False)
                    self.spinBox.setValue(0)
                    self.spinBox_2.setValue(0)
                    self.spinBox_3.setValue(0)
                    self.spinBox_4.setValue(0)
                    self.spinBox_5.setValue(0)
                    self.spinBox_6.setValue(0)
                    self.spinBox_7.setValue(0)
                    self.spinBox_8.setValue(0)
                    self.spinBox_9.setValue(0)
                    self.spinBox_10.setValue(0)
                    self.spinBox_11.setValue(0)
                    self.spinBox_12.setValue(0)
                    self.spinBox_13.setValue(0)
                    self.spinBox_14.setValue(0)
                    self.spinBox_15.setValue(0)
                    self.spinBox_16.setValue(0)
                    self.spinBox_17.setValue(0)
                    self.spinBox_18.setValue(0)
                    self.spinBox_19.setValue(0)
                    self.spinBox_20.setValue(0)
                else:   # 静态连接方式
                    self.radioButton_2.setChecked(False)
                    self.radioButton.setChecked(True)
                    self.groupBox_4.setEnabled(True)
                    self.groupBox_6.setEnabled(True)
                    self.groupBox_8.setEnabled(True)
                    self.groupBox_10.setEnabled(True)
                    self.groupBox_12.setEnabled(True)
                    objective_ip = ip.split('.')   # 按'.'将字符串分割成列表
                    self.spinBox.setValue(int(objective_ip[3]))
                    self.spinBox_2.setValue(int(objective_ip[2]))
                    self.spinBox_3.setValue(int(objective_ip[1]))
                    self.spinBox_4.setValue(int(objective_ip[0]))

                    netmask = self.device_data[mac]['netmask'].split('.')   # 按'.'将字符串分割成列表
                    self.spinBox_5.setValue(int(netmask[3]))
                    self.spinBox_6.setValue(int(netmask[2]))
                    self.spinBox_7.setValue(int(netmask[1]))
                    self.spinBox_8.setValue(int(netmask[0]))

                    gateway = self.device_data[mac]['gateway'].split('.')  # 按'.'将字符串分割成列表
                    self.spinBox_9.setValue(int(gateway[3]))
                    self.spinBox_10.setValue(int(gateway[2]))
                    self.spinBox_11.setValue(int(gateway[1]))
                    self.spinBox_12.setValue(int(gateway[0]))

                    dns = self.device_data[mac]['dns1'].split('.')  # 按'.'将字符串分割成列表
                    self.spinBox_13.setValue(int(dns[3]))
                    self.spinBox_14.setValue(int(dns[2]))
                    self.spinBox_15.setValue(int(dns[1]))
                    self.spinBox_16.setValue(int(dns[0]))

                    dns_flag = self.device_data[mac]['dns2'].split('.')  # 按'.'将字符串分割成列表
                    self.spinBox_17.setValue(int(dns_flag[3]))
                    self.spinBox_18.setValue(int(dns_flag[2]))
                    self.spinBox_19.setValue(int(dns_flag[1]))
                    self.spinBox_20.setValue(int(dns_flag[0]))

        except Exception as e:
            print(traceback.print_exc())


    def CLEAR_DATA_WINDOW(self):
        '''清除界面数据'''
        try:
            self.spinBox.setValue(0)
            self.spinBox_2.setValue(0)
            self.spinBox_3.setValue(0)
            self.spinBox_4.setValue(0)

            self.spinBox_5.setValue(0)
            self.spinBox_6.setValue(0)
            self.spinBox_7.setValue(0)
            self.spinBox_8.setValue(0)

            self.spinBox_9.setValue(0)
            self.spinBox_10.setValue(0)
            self.spinBox_11.setValue(0)
            self.spinBox_12.setValue(0)

            self.spinBox_13.setValue(0)
            self.spinBox_14.setValue(0)
            self.spinBox_15.setValue(0)
            self.spinBox_16.setValue(0)

            self.spinBox_17.setValue(0)
            self.spinBox_18.setValue(0)
            self.spinBox_19.setValue(0)
            self.spinBox_20.setValue(0)
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
    myWin = changeIP_single()
    myWin.show()
    sys.exit(app.exec_())