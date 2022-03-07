import sys
import traceback
from shuncom_ui.window_son.restart_ui.tool_reboot import Ui_tool_reboot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QCursor
from tzlocal import get_localzone
from PyQt5 import QtCore, QtWidgets, QtGui
from shuncom_module.shuncom_fun import *
class ReBoot(QMainWindow, Ui_tool_reboot):
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    reboot_window_exit_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(ReBoot, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.lastip = None  # 上次被选中的单个ip
        self.selectstate = 0  # 选中状态
        self.restart_data = {}  # 定时重启数据
        self.device_data = {}  # 被选中的设备信息

    def initUI(self):
        '''界面控件绑定'''
        self.pushButton_2.clicked.connect(self.Exit_window_func)
        self.pushButton.clicked.connect(self.SAVE_DATA_WINDOW)
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)  # 窗口置顶
            self.add_shadow(self.comboBox)
            self.add_shadow(self.groupBox_5)
            self.add_shadow(self.pushButton_2)
        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################

    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)

    ############################################自写函数#########################################

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

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.reboot_window_exit_signal.emit()

    def Exit_window_func(self):
        '''退出界面函数'''
        try:
            self.selectstate = 0
            self.close()
        except Exception as e:
            print(traceback.print_exc())


    def SAVE_DATA_WINDOW(self):
        '''保留界面数据'''
        try:
            if self.radioButton.isChecked() == True:
                self.restart_data.clear()
                self.restart_data['enable'] = '0'
            else:
                self.restart_data['enable'] = '1'
                if self.comboBox.currentIndex() == 0:
                    self.restart_data['days'] = "1,2,3,4,6,5,7"
                else:
                    self.restart_data['days'] = str(self.comboBox.currentIndex())


                restart_time = self.timeEdit.text()
                hour, min = time_zone_offset(restart_time)
                self.restart_data['hour'] = hour
                self.restart_data['min'] = min
            print(self.restart_data)
            self.selectstate = 1
            self.close()
        except Exception as e:
            print(traceback.print_exc())



    def window_updata(self):
        try:
            mac_list = list(self.device_data.keys())
            # print(self.device_data)
            self.label_9.setText(str(len(mac_list)))
            self.radioButton_2.setChecked(True)
            self.radioButton.setChecked(False)
            self.comboBox.setCurrentIndex(0)
            self.timeEdit.setTime(QTime(0, 0, 0))
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
    myWin = ReBoot()
    myWin.show()
    sys.exit(app.exec_())