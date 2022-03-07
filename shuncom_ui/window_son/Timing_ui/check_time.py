import sys
import traceback
from shuncom_ui.window_son.Timing_ui.tool_check_time import Ui_tool_check_time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui
from shuncom_module.shuncom_fun import *
class Check_Time(QMainWindow, Ui_tool_check_time):
    cheaktime_window_exit_signel = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(Check_Time, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.Timing_data = {}  # 校时数据
        self.device_data = {}  # 被选中的设备信息
    def initUI(self):
        '''界面控件绑定'''
        self.pushButton.clicked.connect(self.Enter_action)  # 退出界面
        self.pushButton_2.clicked.connect(self.Exit_window_func)  # 确认按键动作
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号


    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)  # 窗口置顶
            self.add_shadow(self.lineEdit)
            self.add_shadow(self.lineEdit_2)
            self.add_shadow(self.groupBox_5)
            self.add_shadow(self.pushButton_2)
        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.cheaktime_window_exit_signel.emit()

    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)

    ##########################################自定义功能函数#######################################
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

    def Enter_action(self):
        '''确定按键动作'''
        try:
            if len(self.device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('警告', '未勾选设备!')
                return
            if self.radioButton.isChecked() == True:
                self.Timing_data['enabled'] = '1'
                self.Timing_data['server'] = self.lineEdit.text()
                self.Timing_data['port'] = self.lineEdit_2.text()

                self.Timing_data['sync_interval'] = str(int(self.lineEdit_3.text()) * 60)
            else:
                self.Timing_data['enabled'] = '0'
            print(self.Timing_data)
            self.selectstate = 1
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def window_updata(self):
        try:
            mac_list = list(self.device_data.keys())
            # print(self.device_data)
            self.label_9.setText(str(len(mac_list)))

        except Exception as e:
            print(traceback.print_exc())

    def window_init(self):
        '''界面数据初始化'''
        try:
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
            self.lineEdit.setText('')
            self.lineEdit_3.setText('')
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
    myWin = Check_Time()
    myWin.show()
    sys.exit(app.exec_())