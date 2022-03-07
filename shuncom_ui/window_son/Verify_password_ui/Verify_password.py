###############################系统模块###############################
import sys
import traceback
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QGraphicsDropShadowEffect
#############################自定义模块###############################
from shuncom_ui.window_son.Verify_password_ui.password import Ui_MainWindow
from shuncom_module.shuncom_log_init import sz_log_Error, sz_log_record

class Verify_password(QMainWindow, Ui_MainWindow):
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    def __init__(self):
        super(Verify_password, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.password = ''

    def initUI(self):
        '''界面控件绑定'''
        self.pushButton.clicked.connect(self.close)     # 取消键
        self.pushButton_2.clicked.connect(self.save_window_password)   # 确认键
        self.lineEdit.returnPressed.connect(self.save_window_password)  # 输入栏回车快捷
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.lineEdit.setText('')

    def save_window_password(self):
        try:
            self.password = self.lineEdit.text()
            print(self.password)
            self.close()
        except Exception as e:
            print(traceback.print_exc())

    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)# 窗口置顶
            self.add_shadow(self.lineEdit)
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
            sz_log_Error.error('给控件添加白色阴影 异常: %s' % e)

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
            sz_log_Error.error('给按钮添加阴影效果 异常: %s' % e)

    def center(self, position):  # 定义一个函数使得窗口居中显示
        # 获取主窗口的中心
        main_center = [position[0] + position[2] / 2, position[1] + position[3] / 2]
        # 计算子窗口要显示的位置
        show_x = main_center[0] - self.width() / 2
        show_y = main_center[1] - self.height() / 2
        self.move(show_x, show_y)

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
    myWin = Verify_password()
    myWin.show()
    sys.exit(app.exec_())
