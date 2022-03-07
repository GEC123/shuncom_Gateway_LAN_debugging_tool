import sys
import os
import traceback
from shuncom_ui.window_son.upgrade_ui.tool_firmware_update import Ui_tool_firmware_update
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui

class Firmware_Update(QMainWindow, Ui_tool_firmware_update):
    updata_window_exit_signal = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super(Firmware_Update, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.filename = ''  # 选择固件的路径
        self.device_data = {}  # 被选中的设备信息

    def initUI(self):
        '''界面控件绑定'''
        self.pushButton.clicked.connect(self.AddFile)
        self.pushButton_2.clicked.connect(self.Enter_Updata)
        self.pushButton_3.clicked.connect(self.Exit_window_func)
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)  # 窗口置顶
            self.add_shadow(self.pushButton)
            self.add_shadow(self.pushButton_3)
            self.add_shadow(self.lineEdit)
        except Exception as e:
            print(traceback.print_exc())

    ###########################################官方函数重写#########################################
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.updata_window_exit_signal.emit()

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

    def AddFile(self):
        '''添加文件'''
        try:
            self.filename, ok = QtWidgets.QFileDialog.getOpenFileName(self, "选择添加文件", '', "Text Files(*.bin)")
            self.lineEdit.setText(self.filename)
        except Exception as e:
            print(traceback.print_exc())

    def Exit_window_func(self):
        '''退出界面操作'''
        try:
            self.selectstate = 0
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def Enter_Updata(self):
        '''确认升级'''
        try:
            if os.path.exists(self.lineEdit.text()) == True:
                pass
            else:
                self.signal_Popup_Qtime_QtCore.emit('提示', '文件不存在!')
                return
            if self.check_device_storage_size() == False:
                return
            self.selectstate = 1
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def check_device_storage_size(self):
        '''检测设备剩余内存'''
        try:
            firmware_size = os.path.getsize(self.lineEdit.text())
            print(firmware_size, type(firmware_size))
            mac_list = list(self.device_data.keys())
            for mac in mac_list:
                if firmware_size > int(self.device_data[mac]['storage_size']):
                    result = QMessageBox.information(self, '提示', '有设备剩余内存不足，是否继续?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if result == QMessageBox.Yes:
                        return True
                    else:
                        return False
            return True
        except Exception as e:
            print(traceback.print_exc())

    def window_updata(self):
        try:
            mac_list = list(self.device_data.keys())
            self.label_4.setText(str(len(mac_list)))
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
    myWin = Firmware_Update()
    myWin.show()
    sys.exit(app.exec_())