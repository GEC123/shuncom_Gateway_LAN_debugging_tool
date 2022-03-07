import json
import re
import sys
import traceback
from shuncom_ui.window_son.change_server_ui.tool_change_server_point import Ui_tool_change_server_point
from shuncom_ui.window_son.add_server_pointing_ui.add_server_pointing import AddServerPointing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore, QtWidgets, QtGui


class change_server(QMainWindow, Ui_tool_change_server_point):
    server_windoow_exit_signal = QtCore.pyqtSignal()
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    flash_show_mode_Qtime_QtCore = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        super(change_server, self).__init__(parent)
        self.Add_Server_Pointing_window = AddServerPointing()
        self.setupUi(self)
        self.initUI()
        self.SET_UI_QSS()
        self.selectstate = 0  # 选择状态
        self.WindowShowModule = 'MORE'  # 两种界面显示模式: MORE SIGNLE (界面显示模式默认为多设备模式)
        self.ServerDATA = {}  # 保留界面数据
        self.lastselect = None  # 上一次表格选项
        self.lastip = None  # 上一次操作的IP
        self.device_data = {}  # 被选中的设备信息
        self.Server_key_list = []   # 服务器键值队列
        self.SeverListData = {'sziot': {}, 'sztt': {}, 'mqtt': {}}  # 每个服务器的数据

        self.mode_1.close()
        self.mode_2.close()
        self.mode_3.close()
        self.label_9.close()
        self.lineEdit_9.close()
        self.label_35.close()
        self.lineEdit_13.close()
        self.label_10.close()
        self.lineEdit_2.close()
        self.label_36.close()
        self.lineEdit_14.close()
        self.label_37.close()
        self.comboBox_2.close()

    def initUI(self):
        '''界面控件绑定'''
        self.flash_show_mode_Qtime_QtCore.connect(self.flash_show_mode)  # 显示信号绑定
        self.tableWidget.clicked.connect(self.flash_show_mode_Qtime_QtCore.emit)  # 判断点击的表格内容

        self.pushButton.clicked.connect(self.show_add_server_window)  # 显示增加服务器指向窗口
        self.pushButton_2.clicked.connect(self.delect_server_pointing)  # 删除服务器指向
        self.pushButton_3.clicked.connect(self.Exit_window_func)
        self.pushButton_4.clicked.connect(self.Enter_action)    # 确认按键动作
        '''信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号
        self.Add_Server_Pointing_window.Exit_signal_Qtime_QtCore.connect(self.sonwindow_exit_flash) #子界面退出调用

    def SET_UI_QSS(self):
        try:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)  # 窗口置顶
            self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
            self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置全列不可编辑
            '''灰色阴影添加'''
            self.add_shadow(self.pushButton)
            self.add_shadow(self.pushButton_2)
            self.add_shadow(self.pushButton_3)
            self.add_shadow(self.comboBox)
            self.add_shadow(self.lineEdit)
            self.add_shadow(self.groupBox_3, value=10)
            self.add_shadow(self.groupBox_2, value=10)
            ##############mode_1################
            self.add_shadow(self.lineEdit_9)
            self.add_shadow(self.lineEdit_13)
            self.add_shadow(self.lineEdit_14)
            self.add_shadow(self.lineEdit_15)
            self.add_shadow(self.comboBox_2)
            self.add_shadow(self.lineEdit_2)
            self.add_shadow(self.lineEdit_3)
            ##############mode_2################
            self.add_shadow(self.lineEdit_16)
            self.add_shadow(self.lineEdit_4)
            self.add_shadow(self.lineEdit_5)
            self.add_shadow(self.lineEdit_6)
            self.add_shadow(self.lineEdit_7)
            self.add_shadow(self.lineEdit_8)
            self.add_shadow(self.comboBox_5)
            ##############mode_3################
            self.add_shadow(self.comboBox_3)
            self.add_shadow(self.comboBox_4)
            self.add_shadow(self.lineEdit_17)
            self.add_shadow(self.lineEdit_10)
            self.add_shadow(self.lineEdit_11)
            self.add_shadow(self.lineEdit_12)

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
            effect_shadow.setOffset(0, 0)  # 设置偏移量
            effect_shadow.setBlurRadius(value)  # 设置阴影范围
            effect_shadow.setColor(QtCore.Qt.gray)  # 设置阴影颜色为灰色
            pushbutton.setGraphicsEffect(effect_shadow)  # 将阴影加入到按钮
        except Exception as e:
            print(traceback.print_exc())


    def show_add_server_window(self):
        '''显示增加服务器指向窗口'''
        try:
            self.Add_Server_Pointing_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            self.Add_Server_Pointing_window.center(position)
            tabledata = []
            for row in range(self.tableWidget.rowCount()):
                tabledata.append(self.tableWidget.item(row, 0).text())
            self.Add_Server_Pointing_window.GetHomeTabDate(tabledata)
            self.Add_Server_Pointing_window.show()
        except Exception as e:
            print(traceback.print_exc())

    def sonwindow_exit_flash(self):
        '''子界面退出刷新主界面'''
        try:
            if len(self.Add_Server_Pointing_window.SeverInfo) == 0:
                return
            sonwindow_data = self.Add_Server_Pointing_window.SeverInfo
            # print(sonwindow_data)
            rownum = self.tableWidget.rowCount()
            name = sonwindow_data['连接名称']
            connect_type = sonwindow_data['协议类型']
            self.tableWidget.setRowCount(rownum + 1)
            self.tableWidget.setItem(rownum, 0, QtWidgets.QTableWidgetItem('%s(%s)' % (name, connect_type)))
            ip_port = sonwindow_data['服务器IP'] + ':' + sonwindow_data['端口']
            if connect_type == 'sziot':
                self.SeverListData['sziot'][ip_port] = {}
                self.SeverListData['sziot'][ip_port]['proto'] = 'tcp'  # 新增sziot连接类型默认使用tcp协议
                self.SeverListData['sziot'][ip_port]['encryption'] = 'aes128'  # 加密
                self.SeverListData['sziot'][ip_port]['compress'] = 'zip'  # 压缩
            elif connect_type == 'Touchuan':
                self.SeverListData['sztt'][ip_port] = {}
                self.SeverListData['sztt'][ip_port]['datasrc'] = 'RS485-1'  # 数据来源
                self.SeverListData['sztt'][ip_port]['heartbeat_type'] = 'off'  # 心跳类型
                self.SeverListData['sztt'][ip_port]['register_type'] = 'off'  # 注册类型
                self.SeverListData['sztt'][ip_port]['heartbeat_interval'] = 60  # 心跳间隔
            else:
                self.SeverListData['mqtt'][ip_port] = {}
                self.SeverListData['mqtt'][ip_port]['mqtt_broker'] = 'common'
                self.SeverListData['mqtt'][ip_port]['"username"'] = ''  # 用户名
                self.SeverListData['mqtt'][ip_port]['passwd'] = ''  # 密码
                self.SeverListData['mqtt'][ip_port]['host'] = sonwindow_data['服务器IP']  # IP
                self.SeverListData['mqtt'][ip_port]['port'] = sonwindow_data['端口']  # 端口
                self.SeverListData['mqtt'][ip_port]['pubqos'] = 2  # 发布Qos

            self.Server_key_list.append(ip_port)

            self.save_last_select_data()  # 保存上次数据
            # print(self.Server_key_list)
            self.tableWidget.item(rownum, 0).setSelected(True)
            self.flash_show_mode()
            self.Add_Server_Pointing_window.SeverInfo = {}  # 清除添加服务器界面保存的数据
        except Exception as e:
            print(traceback.print_exc())

    def delect_server_pointing(self):
        '''删除服务器指向'''
        try:
            row_select = self.tableWidget.selectedItems()
            row = row_select[0].row()
            name_type = self.tableWidget.item(row, 0).text()
            connect_type = re.findall(r"\((.*)\)", name_type)[0]  # 确定服务类型
            delect_ip_port = self.Server_key_list.pop(row)
            if connect_type == 'sziot':
                self.SeverListData['sziot'].pop(delect_ip_port)
            elif connect_type == 'Touchuan':
                self.SeverListData['sztt'].pop(delect_ip_port)
            else:
                self.SeverListData['mqtt'].pop(delect_ip_port)

            self.tableWidget.removeRow(row)

        except Exception as e:
            print(traceback.print_exc())

    def save_last_select_data(self):
        '''保存上一次选择的数据'''
        try:
            if self.lastselect not in self.Server_key_list:
                return
            ip_port = self.lastselect
            ip = ip_port.split(':')[0]
            port = ip_port.split(':')[1]
            for lable in range(len(self.Server_key_list)):
                if self.Server_key_list[lable] == self.lastselect:
                    name_type = self.tableWidget.item(lable, 0).text()
                    break
            connect_type = re.findall(r"\((.*)\)", name_type)[0]  # 确定服务类型
            if connect_type == 'sziot':
                # 1、查看IP地址和端口是否被修改
                if ip != self.lineEdit_15.text() or port != self.lineEdit_3.text():
                    new_ip_port = self.lineEdit_15.text() + ':' + self.lineEdit_3.text()
                    self.SeverListData['sziot'][new_ip_port] = self.SeverListData['sziot'].pop(ip_port)
                    ip_port = new_ip_port
                    self.lastselect = ip_port
                    self.Server_key_list[lable] = self.lastselect

                self.SeverListData['sziot'][ip_port].clear()
                # 2、查看选择的协议类型
                if self.radioButton.isChecked() == True:
                    self.SeverListData['sziot'][ip_port]['proto'] = 'tcp'
                    if self.radioButton_3.isChecked() == True:
                        self.SeverListData['sziot'][ip_port]['encryption'] = 'aes128'
                        self.SeverListData['sziot'][ip_port]['compress'] = 'zip'
                    else:
                        self.SeverListData['sziot'][ip_port]['encryption'] = 'none'
                        self.SeverListData['sziot'][ip_port]['compress'] = 'none'
                else:
                    self.SeverListData['sziot'][ip_port]['proto'] = 'mqtt'
                    self.SeverListData['sziot'][ip_port]['user'] = self.lineEdit_9.text()
                    self.SeverListData['sziot'][ip_port]['passwd'] = self.lineEdit_13.text()
                    self.SeverListData['sziot'][ip_port]['subtopic'] = self.lineEdit_2.text()
                    self.SeverListData['sziot'][ip_port]['pubtopic'] = self.lineEdit_14.text()
                    self.SeverListData['sziot'][ip_port]['pubQOS'] = self.comboBox_2.currentText()

            elif connect_type == 'Touchuan':
                # 1、查看IP地址和端口是否被修改
                if ip != self.lineEdit_16.text() or port != self.lineEdit_8.text():
                    new_ip_port = self.lineEdit_16.text() + ':' + self.lineEdit_8.text()
                    self.SeverListData['sztt'][new_ip_port] = self.SeverListData['sztt'].pop(ip_port)
                    ip_port = new_ip_port
                    self.lastselect = ip_port
                    self.Server_key_list[lable] = self.lastselect
                self.SeverListData['sztt'][ip_port].clear()
                self.SeverListData['sztt'][ip_port]['datasrc'] = self.comboBox_5.currentText()
                '''注册类型及数据'''
                if self.radioButton_6.isChecked() == True:
                    self.SeverListData['sztt'][ip_port]['register_type'] = 'off'
                else:
                    if self.radioButton_5.isChecked() == True:
                        self.SeverListData['sztt'][ip_port]['register_type'] = 'hex'
                    else:
                        self.SeverListData['sztt'][ip_port]['register_type'] = 'ascii'
                    self.SeverListData['sztt'][ip_port]['register_data'] = self.lineEdit_4.text()
                '''心跳类型及数据'''
                if self.radioButton_9.isChecked() == True:
                    self.SeverListData['sztt'][ip_port]['heartbeat_type'] = 'off'
                else:
                    if self.radioButton_8.isChecked() == True:
                        self.SeverListData['sztt'][ip_port]['heartbeat_type'] = 'hex'
                    else:
                        self.SeverListData['sztt'][ip_port]['heartbeat_type'] = 'ascii'
                    self.SeverListData['sztt'][ip_port]['heartbeat_data'] = self.lineEdit_5.text()
                self.SeverListData['sztt'][ip_port]['heartbeat_interval'] = self.lineEdit_6.text()

            else:
                # 1、查看IP地址和端口是否被修改
                if ip != self.lineEdit_17.text() or port != self.lineEdit_10.text():
                    new_ip_port = self.lineEdit_17.text() + ':' + self.lineEdit_10.text()
                    self.SeverListData['mqtt'][new_ip_port] = self.SeverListData['mqtt'].pop(ip_port)
                    ip_port = new_ip_port
                    self.lastselect = ip_port
                    self.Server_key_list[lable] = self.lastselect
                self.SeverListData['mqtt'][ip_port].clear()
                self.SeverListData['mqtt'][ip_port]['mqtt_broker'] = self.comboBox_3.currentText()
                self.SeverListData['mqtt'][ip_port]['username'] = self.lineEdit_11.text()
                self.SeverListData['mqtt'][ip_port]['passwd'] = self.lineEdit_12.text()
                self.SeverListData['mqtt'][ip_port]['pubqos'] = self.comboBox_4.currentText()

        except Exception as e:
            print(traceback.print_exc())

    def flash_show_mode(self):
        '''刷新显示模板'''
        try:
            if self.lastselect != None:
                self.save_last_select_data() #保存上一次界面操作后的数据

            row_select = self.tableWidget.selectedItems()
            row = row_select[0].row()  # 选中的行

            data = self.tableWidget.item(row, 0).text()
            connect_type = re.findall(r"\((.*)\)", data)[0]  # 确定服务类型
            name = data.replace('(' + connect_type + ')', '')
            ip_port = self.Server_key_list[row]
            self.lastselect = ip_port
            ip = ip_port.split(':')[0]
            port = ip_port.split(':')[1]
            self.lineEdit.setText(name)

            if connect_type == 'sziot':
                self.comboBox.setCurrentIndex(0)
                self.mode_1.show()
                self.mode_2.close()
                self.mode_3.close()
                self.lineEdit_15.setText(ip)
                self.lineEdit_3.setText(port)
                if self.SeverListData['sziot'][ip_port]['proto'] == 'tcp':
                    self.radioButton.setChecked(True)
                    self.radioButton_2.setChecked(False)
                    self.label_9.close()
                    self.label_35.close()
                    self.label_10.close()
                    self.label_36.close()
                    self.label_37.close()

                    self.lineEdit_9.close()
                    self.lineEdit_13.close()
                    self.lineEdit_2.close()
                    self.lineEdit_14.close()
                    self.comboBox_2.close()
                    self.label_13.show()
                    self.groupBox_10.show()

                    if self.SeverListData['sziot'][ip_port]['encryption'] == 'aes128':
                        self.radioButton_3.setChecked(True)
                        self.radioButton_4.setChecked(False)
                    else:
                        self.radioButton_3.setChecked(False)
                        self.radioButton_4.setChecked(True)
                elif self.SeverListData['sziot'][ip_port]['proto'] == 'mqtt':
                    self.radioButton.setChecked(False)
                    self.radioButton_2.setChecked(True)
                    self.label_9.show()
                    self.label_35.show()
                    self.label_10.show()
                    self.label_36.show()
                    self.label_37.show()
                    self.lineEdit_9.show()
                    self.lineEdit_13.show()
                    self.lineEdit_2.show()
                    self.lineEdit_14.show()
                    self.comboBox_2.show()
                    self.label_13.close()
                    self.groupBox_10.close()
                    self.lineEdit_9.setText(self.SeverListData['sziot'][ip_port]['user'])
                    self.lineEdit_13.setText(self.SeverListData['sziot'][ip_port]['passwd'])
                    self.lineEdit_2.setText(self.SeverListData['sziot'][ip_port]['subtopic'])
                    self.lineEdit_14.setText(self.SeverListData['sziot'][ip_port]['pubtopic'])
                    self.comboBox_5.setCurrentText(str(self.SeverListData['sziot'][ip_port]['pubQOS']))

            elif connect_type == 'Touchuan':
                self.comboBox.setCurrentIndex(1)
                self.mode_1.close()
                self.mode_2.show()
                self.mode_3.close()
                self.lineEdit_16.setText(ip)
                self.lineEdit_8.setText(port)
                self.comboBox_5.setCurrentText(self.SeverListData['sztt'][ip_port]['datasrc'].replace('@MODULE', ''))
                if self.SeverListData['sztt'][ip_port]['register_type'] == 'off':
                    self.radioButton_5.setChecked(False)
                    self.radioButton_6.setChecked(True)
                    self.radioButton_7.setChecked(False)
                    self.label_15.close()
                    self.lineEdit_4.close()
                elif self.SeverListData['sztt'][ip_port]['register_type'] == 'hex':
                    self.radioButton_5.setChecked(True)
                    self.radioButton_6.setChecked(False)
                    self.radioButton_7.setChecked(False)
                    self.label_15.show()
                    self.lineEdit_4.show()
                    self.lineEdit_4.setText(self.SeverListData['sztt'][ip_port]['register_data'])
                else:
                    self.radioButton_5.setChecked(False)
                    self.radioButton_6.setChecked(False)
                    self.radioButton_7.setChecked(True)
                    self.label_15.show()
                    self.lineEdit_4.show()
                    self.lineEdit_4.setText(self.SeverListData['sztt'][ip_port]['register_data'])

                if self.SeverListData['sztt'][ip_port]['heartbeat_type'] == 'off':
                    self.radioButton_8.setChecked(False)
                    self.radioButton_9.setChecked(True)
                    self.radioButton_10.setChecked(False)
                    self.label_17.close()
                    self.lineEdit_5.close()
                elif self.SeverListData['sztt'][ip_port]['heartbeat_type'] == 'hex':
                    self.radioButton_8.setChecked(True)
                    self.radioButton_9.setChecked(False)
                    self.radioButton_10.setChecked(False)
                    self.label_17.show()
                    self.lineEdit_5.show()
                    self.lineEdit_5.setText(self.SeverListData['sztt'][ip_port]['heartbeat_data'])
                else:
                    self.radioButton_8.setChecked(False)
                    self.radioButton_9.setChecked(False)
                    self.radioButton_10.setChecked(True)
                    self.label_17.show()
                    self.lineEdit_5.show()
                    self.lineEdit_5.setText(self.SeverListData['sztt'][ip_port]['heartbeat_data'])

                self.lineEdit_6.setText(str(self.SeverListData['sztt'][ip_port]['heartbeat_interval']))

            else:
                self.comboBox.setCurrentIndex(2)
                self.mode_1.close()
                self.mode_2.close()
                self.mode_3.show()
                self.lineEdit_17.setText(ip)
                self.lineEdit_10.setText(port)
                if 'mqtt_broker' in self.SeverListData['mqtt'][ip_port]:
                    self.comboBox_3.setCurrentText(self.SeverListData['mqtt'][ip_port]['mqtt_broker'])
                else:
                    self.SeverListData['mqtt'][ip_port]['mqtt_broker'] = 'common'
                    self.comboBox_3.setCurrentText(self.SeverListData['mqtt'][ip_port]['mqtt_broker'])
                if 'username' in self.SeverListData['mqtt'][ip_port]:
                    self.lineEdit_11.setText(self.SeverListData['mqtt'][ip_port]['username'])
                else:
                    self.SeverListData['mqtt'][ip_port]['username'] = 'shuncom'
                    self.lineEdit_11.setText(self.SeverListData['mqtt'][ip_port]['username'])

                if 'passwd' in self.SeverListData['mqtt'][ip_port]:
                    self.lineEdit_12.setText(self.SeverListData['mqtt'][ip_port]['passwd'])
                else:
                    self.SeverListData['mqtt'][ip_port]['passwd'] = 'shuncom_passwd'
                    self.lineEdit_12.setText(self.SeverListData['mqtt'][ip_port]['passwd'])
                self.comboBox_4.setCurrentText(str(self.SeverListData['mqtt'][ip_port]['pubqos']))


        except Exception as e:
            print(traceback.print_exc())

    def Data_sorting(self, mac_list):
        '''数据整理'''
        try:
            # print(self.device_data)
            sziot_original_list = self.device_data[mac_list[0]]['sziot']
            sztt_original_list = self.device_data[mac_list[0]]['sztt_cloud']
            mqtt_original_list = self.device_data[mac_list[0]]['mqtt_server']
            # 整理sziot服务器数据
            sziot_num = len(sziot_original_list)
            for sziot_lable in range(sziot_num):
                ip_port = list(sziot_original_list[sziot_lable].keys())[0]
                self.SeverListData['sziot'][ip_port] = {}  # IP加端口
                self.SeverListData['sziot'][ip_port]['proto'] = sziot_original_list[sziot_lable][ip_port]['proto']  # 连接方式
                if self.SeverListData['sziot'][ip_port]['proto'] == 'tcp':
                    self.SeverListData['sziot'][ip_port]['encryption'] = sziot_original_list[sziot_lable][ip_port][
                        'encryption']  # 是否加密
                    self.SeverListData['sziot'][ip_port]['compress'] = sziot_original_list[sziot_lable][ip_port][
                        'compress']  # 是否压缩
                elif self.SeverListData['sziot'][ip_port]['proto'] == 'mqtt':
                    self.SeverListData['sziot'][ip_port]['user'] = sziot_original_list[sziot_lable][ip_port]['user']  # 用户名
                    self.SeverListData['sziot'][ip_port]['passwd'] = sziot_original_list[sziot_lable][ip_port][
                        'passwd']  # 密码
                    self.SeverListData['sziot'][ip_port]['subtopic'] = sziot_original_list[sziot_lable][ip_port][
                        'subtopic']  # 订阅主题
                    self.SeverListData['sziot'][ip_port]['pubtopic'] = sziot_original_list[sziot_lable][ip_port][
                        'pubtopic']  # 发布主题
                    self.SeverListData['sziot'][ip_port]['pubQOS'] = sziot_original_list[sziot_lable][ip_port][
                        'pubQOS']  # 发布QoS
                    self.SeverListData['sziot'][ip_port]['passwd'] = sziot_original_list[sziot_lable][ip_port][
                        'passwd']  # 密码

            # 整理sztt服务器数据
            sztt_num = len(sztt_original_list)
            for sztt_lable in range(sztt_num):
                ip_port = list(sztt_original_list[sztt_lable].keys())[0]
                self.SeverListData['sztt'][ip_port] = {}  # IP加端口
                self.SeverListData['sztt'][ip_port]['datasrc'] = sztt_original_list[sztt_lable][ip_port]['datasrc'].replace(
                    '@MODULE', '')  # 数据来源
                self.SeverListData['sztt'][ip_port]['register_type'] = sztt_original_list[sztt_lable][ip_port][
                    'register_type']  # 注册类型
                if self.SeverListData['sztt'][ip_port]['register_type'] != 'off':
                    self.SeverListData['sztt'][ip_port]['register_data'] = sztt_original_list[sztt_lable][ip_port][
                    'register_data']  # 注册数据
                self.SeverListData['sztt'][ip_port]['heartbeat_type'] = sztt_original_list[sztt_lable][ip_port][
                    'heartbeat_type']  # 心跳类型
                if self.SeverListData['sztt'][ip_port]['heartbeat_type'] != 'off':
                    self.SeverListData['sztt'][ip_port]['heartbeat_data'] = sztt_original_list[sztt_lable][ip_port][
                        'heartbeat_data']  # 心跳数据
                self.SeverListData['sztt'][ip_port]['heartbeat_interval'] = sztt_original_list[sztt_lable][ip_port][
                    'heartbeat_interval']  # 心跳间隔

            # 整理mqtt服务器数据
            mqtt_num = len(mqtt_original_list)
            for mqtt_lable in range(mqtt_num):
                mqtt_broker = list(mqtt_original_list[mqtt_lable].keys())[0]
                ip = mqtt_original_list[mqtt_lable][mqtt_broker]['host']
                port = mqtt_original_list[mqtt_lable][mqtt_broker]['port']  # 端口
                ip_port = ip + ':' + str(port)
                self.SeverListData['mqtt'][ip_port] = {}  # IP加端口
                self.SeverListData['mqtt'][ip_port]['mqtt_broker'] = mqtt_broker  # mqtt_broker
                self.SeverListData['mqtt'][ip_port]['username'] = mqtt_original_list[mqtt_lable][mqtt_broker][
                    'username']  # 用户名
                self.SeverListData['mqtt'][ip_port]['passwd'] = mqtt_original_list[mqtt_lable][mqtt_broker]['passwd']  # 密码
                self.SeverListData['mqtt'][ip_port]['pubqos'] = mqtt_original_list[mqtt_lable][mqtt_broker][
                    'pubqos']  # 发布QoS

            # 生成服务器键值队列
            sziot_key_list = list(self.SeverListData['sziot'].keys())
            sztt_key_list = list(self.SeverListData['sztt'].keys())
            mqtt_key_list = list(self.SeverListData['mqtt'].keys())
            self.Server_key_list = sziot_key_list + sztt_key_list + mqtt_key_list
        except Exception as e:
            print(traceback.print_exc())

    def window_updata(self):
        '''界面数据刷新'''
        try:
            mac_list = list(self.device_data.keys())
            # print(self.device_data)
            self.label_4.setText(str(len(mac_list)))

            if len(mac_list) < 1 or len(mac_list) > 1:
                self.WindowShowModule = 'MORE'
                self.tableWidget.setRowCount(0)  # 清除表格中的选项
                self.SeverListData['sziot'].clear()
                self.SeverListData['sztt'].clear()
                self.SeverListData['mqtt'].clear()
                self.lastselect = None
                self.Server_key_list.clear()
                self.clearwindowdata()

            else:
                ip = self.device_data[mac_list[0]]
                if self.lastip == None:
                    self.lastip = ip
                elif self.lastip == ip:
                    return
                self.clearwindowdata()
                self.WindowShowModule = 'SIGNLE'
                self.SeverListData['sziot'].clear()
                self.SeverListData['sztt'].clear()
                self.SeverListData['mqtt'].clear()
                self.lastselect = None
                self.Server_key_list.clear()

                self.Data_sorting(mac_list)  # 整理网关服务器数据
                '''将服务器数据显示到界面上'''
                self.tableWidget.setRowCount(0)  # 表格清零


                rownum_sziot = len(self.SeverListData['sziot'])
                rownum_sztt = len(self.SeverListData['sztt'])
                rownum_mqtt = len(self.SeverListData['mqtt'])
                self.tableWidget.setRowCount(rownum_sziot + rownum_sztt + rownum_mqtt)    # 根据服务器数量设置表格行数
                for row in range(rownum_sziot):
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem('sziot%d(%s)' % (row + 1, 'sziot')))
                for row in range(rownum_sztt):
                    self.tableWidget.setItem(row + rownum_sziot, 0, QtWidgets.QTableWidgetItem('sztt%d(%s)' % (row + 1, 'Touchuan')))
                for row in range(rownum_mqtt):
                    self.tableWidget.setItem(row + rownum_sziot + rownum_sztt, 0, QtWidgets.QTableWidgetItem('mqtt%d(%s)' % (row + 1, 'MQTT')))
        except Exception as e:
            print(traceback.print_exc())

    def clearwindowdata(self):
        '''清理窗口数据'''
        try:
            self.mode_1.close()
            self.mode_2.close()
            self.mode_3.close()
            self.lineEdit.setText('')
            self.comboBox.setCurrentIndex(0)
            '''mode1清理'''
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
            self.label_9.close()
            self.label_35.close()
            self.label_10.close()
            self.label_36.close()
            self.label_37.close()
            self.lineEdit_9.close()
            self.lineEdit_13.close()
            self.lineEdit_2.close()
            self.lineEdit_14.close()
            self.comboBox_2.close()
            self.label_13.show()
            self.groupBox_10.show()
            self.lineEdit_9.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_14.setText('')
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_15.setText('')
            self.lineEdit_3.setText('')
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
            '''mode2清理'''
            self.comboBox_5.setCurrentIndex(0)
            self.radioButton_5.setChecked(True)
            self.radioButton_6.setChecked(False)
            self.radioButton_7.setChecked(False)
            self.lineEdit_4.setText('')
            self.lineEdit_4.show()
            self.radioButton_8.setChecked(True)
            self.radioButton_9.setChecked(False)
            self.radioButton_10.setChecked(False)
            self.lineEdit_5.setText('')
            self.lineEdit_5.show()
            self.lineEdit_6.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_8.setText('')
            '''mode3清理'''
            self.comboBox_3.setCurrentIndex(0)
            self.lineEdit_17.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_12.setText('')
            self.comboBox_4.setCurrentIndex(0)
        except Exception as e:
            print(traceback.print_exc())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.server_windoow_exit_signal.emit()

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
            print(self.SeverListData)
            self.selectstate = 1
            if self.tableWidget.rowCount() != 0:
                row_select = self.tableWidget.selectedItems()
                if row_select != []:
                    row = row_select[0].row()
                    self.lastselect = self.Server_key_list[row]
                    self.save_last_select_data()
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
    myWin = change_server()
    myWin.show()
    sys.exit(app.exec_())
