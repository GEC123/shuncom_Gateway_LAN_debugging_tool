#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员:周标华
# time: 2022-01-19 19:52
# 文件名称: shuncom_main_2.py
# 开发工具: PyCharm
# Version: 1.0.0
"""
声明：加载UI文件
"""

#+++++++++++++++++++++++++++++++++ 系统模块 +++++++++++++++++++++++++++++++++++
import json
import _thread
import hashlib
import os
import time
import traceback
import win32gui
import win32api
import xlsxwriter
import Cython
from splinter import Browser
from selenium import webdriver
from PyQt5.QtGui import QCursor, QDesktopServices, QIcon, QColor
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QComboBox, QToolButton, QMenu, QAction, QItemDelegate, QMessageBox
#++++++++++++++++++++++++++++++++ 功能模块 ++++++++++++++++++++++++++++++++++++++
from shuncom_module.shuncom_fun import *
from shuncom_module.shuncom_log_init import sz_log_Error, sz_log_record
#++++++++++++++++++++++++++++++++ 自定义模块 +++++++++++++++++++++++++++++++++++++
from shuncom_ui.window_son.changeIP_more_ui.changeIP_more import changeIP_more
from shuncom_ui.window_son.changeIP_single_ui.changeIP_single import changeIP_single
from shuncom_ui.window_son.change_Zigbee_ui.change_Zigbee import change_Zigbee
from shuncom_ui.window_son.change_server_ui.change_server_point import change_server
from shuncom_ui.window_son.search_set_ui.shuncom_search_set import search_set_MainWindow
from shuncom_ui.window_son.Reset_ui.factory_reset import Factory_Reset
from shuncom_ui.window_son.restart_ui.reboot import ReBoot
from shuncom_ui.window_son.Timing_ui.check_time import Check_Time
from shuncom_ui.window_son.upgrade_ui.firmware_update import Firmware_Update
from shuncom_ui.window_son.version_information_ui.version_information import version_info
from shuncom_ui.window_son.Administrator_ui.Administrator_login import Administrator
from shuncom_module.shuncom_params_init import * #初始化模块
from shuncom_module.shuncom_sql import * #数据库模块

class ShuncomWidget(MainWindow_main_1):
    """ 加载UI文件 """
    flash_tableWidget_data_Qtcore = QtCore.pyqtSignal()

    def __init__(self):
        super(ShuncomWidget, self).__init__()
        self.setupUi(self)
        '''子窗口初始化'''
        self.search_window = search_set_MainWindow()  # 设置搜索网段窗口初始化
        self.IPsingle_window = changeIP_single()  # 修改单个IP窗口初始化
        self.IPmore_window = changeIP_more()  # 修改多个IP窗口初始化
        self.Server_window = change_server()  # 修改服务器指向窗口初始化
        self.Zigbee_window = change_Zigbee()  # 修改zigbee主栈窗口初始化
        self.Reboot_window = ReBoot()  # 重启窗口初始化
        self.CheakTime_window = Check_Time()  # 校时窗口初始化
        self.Updata_window = Firmware_Update()  # 固件升级窗口初始化
        self.version_window = version_info()  # 版本信息窗口初始化
        self.Administrator_window = Administrator()  # 管理员界面初始化

        '''内置变量定义'''
        self.udp_data = {}
        self.initUI()

        '''程序数据初始化'''
        self.SET_UI_QSS()
        self.set_en_zh_ui()
        self.groupBox_7.close()  # 隐藏更多操作窗口
        self.tableWidget_3.close()  # 隐藏列设置窗口
        self.pushButton_17.close()  # 隐藏管理员登录入口
        self.Init_Window_Data()
        self.pushButton_11.setStyleSheet(QPushButtoStyle2)

        '''启动http服务器'''
        _thread.start_new_thread(bulid_http_server, ())
    def initUI(self):
        """ UI """
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.VerSectionClicked)  # 表头单击信号
        self.tableWidget_3.horizontalHeader().sectionClicked.connect(self.VerSectionClicked_list)  # 列设置单击信号
        self.tableWidget.clicked.connect(self.restore_tablewidget_color_Qtime_QtCore.emit)  # 恢复单元格颜色
        '''界面控件'''
        self.lineEdit.returnPressed.connect(self.tableWidget_search)  # 输入栏回车快捷
        self.pushButton_10.clicked.connect(self.tableWidget_search)  # 点击搜索按钮
        self.pushButton_4.clicked.connect(self.Export_tablewidget_data)  # 导出选中设备的数据
        self.pushButton_2.clicked.connect(lambda: thread_it(self.flash_device))  # 刷新网段设备
        self.pushButton_5.clicked.connect(self.delete_devices)  # 删除设备按键
        self.pushButton_11.clicked.connect(self.SHOW_CLOSE_groupBox_7)  # 显示、关闭更多操作
        self.pushButton_3.clicked.connect(self.SHOW_CLOSE_tableWidget_3)  # 显示、关闭更多操作
        self.tableWidget.doubleClicked.connect(self.search_internet)  # 双击IP进入浏览器
        self.comboBox.currentIndexChanged.connect(self.flash_display_device_type)  # 对列表进行类型筛选

        ################指令操作函数###############
        self.pushButton_14.clicked.connect(self.restore_factory_click_function)  # 恢复出厂设置绑定函数
        self.pushButton_15.clicked.connect(self.restate_now_click_function)  # 立即重启绑定函数
        self.pushButton_16.clicked.connect(self.order_action_function)  # 指令下发动作函数
        self.lineEdit_2.returnPressed.connect(self.order_action_function)  # 指令下发动作函数(回车)
        ################子窗口显示绑定##############
        self.pushButton.clicked.connect(self.search_set)  # 打开设置搜索网段
        self.pushButton_6.clicked.connect(self.IP_show)  # 修改设备IP
        self.pushButton_7.clicked.connect(self.Server_show)  # 修改服务器指向
        self.pushButton_8.clicked.connect(self.Zigbee_show)  # 修改Zigbee主栈
        self.pushButton_12.clicked.connect(self.Updata_show)    # 固件升级
        self.pushButton_13.clicked.connect(self.CheakTime_show)     # 校时
        self.pushButton_9.clicked.connect(self.Reboot_show)    # 定时重启
        self.pushButton_17.clicked.connect(self.Administrator_show)  # 管理员登录

        #################子窗口反馈绑定############
        self.Administrator_window.Administrator_login_Qtime_QtCore.connect(self.Administrator_login_result)  # 登录界面反馈绑定
        self.IPsingle_window.ipsingle_window_exit_signal.connect(self.feedback_change_ip_single)  # 修改单个IP反馈函数
        self.IPmore_window.ipmore_window_exit_signal.connect(self.feedback_change_ip_more)  # 修改多个IP反馈函数
        self.Server_window.server_windoow_exit_signal.connect(self.feedback_change_server)  # 修改服务器窗口反馈函数
        self.Zigbee_window.zigbee_window_exit_signal.connect(self.feedback_change_zigbee)  # 修改zigbee窗口反馈函数
        self.Updata_window.updata_window_exit_signal.connect(self.feedback_updata)  # 固件升级窗口反馈函数
        self.CheakTime_window.cheaktime_window_exit_signel.connect(self.feedback_cheak_timing)  # 校时窗口退出反馈函数
        self.Reboot_window.reboot_window_exit_signal.connect(self.feedback_timing_reboot)  # 定时重启反馈绑定

        '''自定义信号绑定'''
        self.signal_Popup_Qtime_QtCore.connect(self.signal_Popup)  # 弹窗信号
        self.flash_table_number_Qtime_QtCore.connect(self.FlashNumber)  # 刷新表格序号
        self.flash_tableWidget_data_Qtcore.connect(self.flash_tableWidget_data)  # 更新数据
        self.set_tablewidget_color_Qtime_QtCore.connect(self.set_select_tablewidget_color)  # 设置选中单元格字体、背景
        self.set_error_device_table_color_Qtime.connect(self.set_error_device_table_color)  # 设置指令请求出错的设备单元格颜色
        self.restore_tablewidget_color_Qtime_QtCore.connect(self.restore_tablewidget_color)  # 复原单元格字体、背景
        self.tablewidget_item_updata_Qtime_QtCore.connect(self.tableWidget_item_updata)  # 表格单元格数据更新信号
        '''右键菜单'''
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 选中的行
        self.tableWidget.customContextMenuRequested[QtCore.QPoint].connect(self.tableWidget_right_Menu)  # 设置表13的右键菜单


    #+++++++++++++++++++++++++++++数据处理函数++++++++++++++++++++++++++++++++++++++
    def find_column_table(self, name):
        """查找列所在的下标"""
        try:
            # 获取当前表格中列表的列名并保存
            list_name = []
            for column in range(self.tableWidget.columnCount()):
                list_name.append(self.tableWidget.horizontalHeaderItem(column).text())
            i = 0
            while i < len(list_name):
                if name == list_name[i]:
                    return i
                i += 1
            return None
        except Exception as e:
            sz_log_Error.error('find_column_table 异常: %s' % e)
            print(traceback.print_exc())

    def flash_display_device_type(self):
        '''设备类型筛选函数'''
        try:
            device_type = self.comboBox.currentText()
            rownum = self.tableWidget.rowCount()

            for row in range(rownum):
                self.tableWidget.showRow(row)

            if device_type == '全部':
                return
            else:
                column = self.find_column_table('设备类别')
                for row in range(rownum):
                    if self.tableWidget.item(row, column).text() != device_type:
                        self.tableWidget.hideRow(row)
        except Exception as e:
            print(traceback.print_exc())

    def add_device(self, device_data, online_status):
        """添加设备"""
        try:
            if device_data == None:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未扫描到设备!')
                return
            key_list = list(device_data.keys())     # keys得到元组强制成列表
            for row in range(len(device_data)):
                device_type = device_data[key_list[row]]['device_type']     # 设备类别
                
                IP = device_data[key_list[row]]['ipaddr']  # IP地址
                MAC = key_list[row]  # MAC地址
                Firmware_version = device_data[key_list[row]]['version']  # 固件版本
                Hardware_model = device_data[key_list[row]]['HW_model']  # 硬件版本
                Connection_mode = device_data[key_list[row]]['proto']  # 连接方式
                http_port = device_data[key_list[row]]['http_port']    # HTTP端口
                netmask = device_data[key_list[row]]['netmask']       # 子网掩码
                channel = device_data[key_list[row]]['channel']       # Zigbee频点
                pan_id = device_data[key_list[row]]['pan_id']       # Zigbee频点ID
                seiot_list = []     # SZIOT服务器列表
                if device_data[key_list[row]]['sziot'] != {}:
                    if len(device_data[key_list[row]]['sziot']) >= 1:
                        seiot_data = device_data[key_list[row]]['sziot']
                        sziot_num = len(seiot_data)
                        for i in range(sziot_num):
                            seiot_list.append(list(seiot_data[i].keys())[0])
                sztt_list = []      # SZTT服务器列表
                if device_data[key_list[row]]['sztt_cloud'] != {}:
                    if len(device_data[key_list[row]]['sztt_cloud']) >= 1:
                        sztt_data = device_data[key_list[row]]['sztt_cloud']
                        sztt_num = len(sztt_data)
                        for i in range(sztt_num):
                            sztt_list.append(list(sztt_data[i].keys())[0])
                mqtt_list = []      # MQTT服务器列表
                if device_data[key_list[row]]['mqtt_server'] != {}:
                    # print(device_data[key_list[row]]['mqtt_server'])
                    if len(device_data[key_list[row]]['mqtt_server']) >= 1:
                        mqtt_data = device_data[key_list[row]]['mqtt_server']
                        mqtt_num = len(mqtt_data)
                        for i in range(mqtt_num):
                            key = list(mqtt_data[i].keys())[0]
                            # print(i, key)
                            mqtt_ip_port = mqtt_data[i][key]['host'] + ':' + str(mqtt_data[i][key]['port'])
                            mqtt_list.append(mqtt_ip_port)

                row = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(row + 1)
                self.Add_tableWidget_row(row)  # 添加新行控件

                lable_device_type = self.find_column_table('设备类别')
                if lable_device_type is not None:
                    self.tableWidget.setItem(row, lable_device_type, QtWidgets.QTableWidgetItem(device_type))  # 设备类别
                    self.tableWidget.item(row, lable_device_type).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                lable_mac = self.find_column_table('MAC地址')
                if lable_mac is not None:
                    self.tableWidget.setItem(row, lable_mac, QtWidgets.QTableWidgetItem(MAC))  # MAC地址
                    self.tableWidget.item(row, lable_mac).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_ip = self.find_column_table('设备IP地址')
                if lable_ip is not None:
                    self.tableWidget.setItem(row, lable_ip, QtWidgets.QTableWidgetItem(IP))  # IP地址
                    self.tableWidget.item(row, lable_ip).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_ver = self.find_column_table('固件版本号')
                if lable_ver is not None:
                    self.tableWidget.setItem(row, lable_ver, QtWidgets.QTableWidgetItem(Firmware_version))  # 固件版本
                    self.tableWidget.item(row, lable_ver).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_HW = self.find_column_table('硬件型号')
                if lable_HW is not None:
                    self.tableWidget.setItem(row, lable_HW, QtWidgets.QTableWidgetItem(Hardware_model))  # 硬件型号
                    self.tableWidget.item(row, lable_HW).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_proto = self.find_column_table('连接方式')
                if lable_proto is not None:
                    self.tableWidget.setItem(row, lable_proto, QtWidgets.QTableWidgetItem(Connection_mode))  # 连接方式
                    self.tableWidget.item(row, lable_proto).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_http = self.find_column_table('HTTP端口')
                if lable_http is not None:
                    self.tableWidget.setItem(row, lable_http, QtWidgets.QTableWidgetItem(http_port))  # HTTP端口
                    self.tableWidget.item(row, lable_http).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_netmask = self.find_column_table('子网掩码')
                if lable_netmask is not None:
                    self.tableWidget.setItem(row, lable_netmask, QtWidgets.QTableWidgetItem(netmask))  # 子网掩码
                    self.tableWidget.item(row, lable_netmask).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                lable_sziot = self.find_column_table('SZIOT服务器IP地址:端口')
                if lable_sziot is not None:
                    if len(seiot_list) > 1:
                        combox = QComboBox()
                        combox.setEditable(True)
                        if online_status == 'online':
                            combox.setStyleSheet(comboxBarStyle)
                        else:
                            combox.setStyleSheet(comboxBarStyle_offline)
                        for sziot in seiot_list:
                            combox.addItem(sziot)
                        self.tableWidget.setCellWidget(row, lable_sziot, combox)

                    elif len(seiot_list) == 1:
                        sziot_data = seiot_list[0]
                        self.tableWidget.setItem(row, lable_sziot, QtWidgets.QTableWidgetItem(str(sziot_data)))  # SZIOT服务器IP地址:端口
                        self.tableWidget.item(row, lable_sziot).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # 设置单元格垂直水平居中
                    else:
                        self.tableWidget.setItem(row, lable_sziot, QtWidgets.QTableWidgetItem('无'))  # SZIOT服务器IP地址:端口
                        self.tableWidget.item(row, lable_sziot).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置单元格垂直水平居中

                lable_sztt = self.find_column_table('SZTT服务器IP地址:端口')
                if lable_sztt is not None:
                    if len(sztt_list) > 1:
                        combox = QComboBox()
                        combox.setEditable(True)
                        if online_status == 'online':
                            combox.setStyleSheet(comboxBarStyle)
                        else:
                            combox.setStyleSheet(comboxBarStyle_offline)
                        for sztt in sztt_list:
                            combox.addItem(sztt)
                        self.tableWidget.setCellWidget(row, lable_sztt, combox)
                    elif len(sztt_list) == 1:
                        sztt_data = sztt_list[0]
                        self.tableWidget.setItem(row, lable_sztt, QtWidgets.QTableWidgetItem(str(sztt_data)))  # SZTT服务器IP地址:端口
                        self.tableWidget.item(row, lable_sztt).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # 设置单元格垂直水平居中
                    else:
                        self.tableWidget.setItem(row, lable_sztt, QtWidgets.QTableWidgetItem('无'))  # SZTT服务器IP地址:端口
                        self.tableWidget.item(row, lable_sztt).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置单元格垂直水平居中

                lable_mqtt = self.find_column_table('MQTT服务器IP地址:端口')
                if lable_mqtt is not None:
                    if len(mqtt_list) > 1:
                        combox = QComboBox()
                        combox.setEditable(True)
                        if online_status == 'online':
                            combox.setStyleSheet(comboxBarStyle)
                        else:
                            combox.setStyleSheet(comboxBarStyle_offline)
                        for mqtt in mqtt_list:
                            combox.addItem(mqtt)
                        self.tableWidget.setCellWidget(row, lable_mqtt, combox)
                    elif len(mqtt_list) == 1:
                        mqtt_data = mqtt_list[0]
                        self.tableWidget.setItem(row, lable_mqtt, QtWidgets.QTableWidgetItem(str(mqtt_data)))  # MQTT服务器IP地址:端口
                        self.tableWidget.item(row, lable_mqtt).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # 设置单元格垂直水平居中
                    else:
                        self.tableWidget.setItem(row, lable_mqtt, QtWidgets.QTableWidgetItem('无'))  # MQTT服务器IP地址:端口
                        self.tableWidget.item(row, lable_mqtt).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置单元格垂直水平居中


                lable_channel = self.find_column_table('Zigbee频点')
                if lable_channel is not None:
                    self.tableWidget.setItem(row, lable_channel, QtWidgets.QTableWidgetItem(str(channel)))  # Zigbee频点
                    self.tableWidget.item(row, lable_channel).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                lable_pan_id = self.find_column_table('Zigbee频点ID')
                if lable_pan_id is not None:
                    if pan_id != '无':
                        self.tableWidget.setItem(row, lable_pan_id, QtWidgets.QTableWidgetItem(D_to_H(pan_id)))  # Zigbee频点ID
                    else:
                        self.tableWidget.setItem(row, lable_pan_id, QtWidgets.QTableWidgetItem(pan_id))  # Zigbee频点ID
                    self.tableWidget.item(row, lable_pan_id).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # 设置单元格垂直水平居中

                if online_status != 'online':
                    column_num = self.tableWidget.columnCount()
                    for column in range(column_num):
                        if self.tableWidget.item(row, column) != None:
                            self.tableWidget.item(row, column).setFlags(self.tableWidget.item(row, column).flags() & ~Qt.ItemIsEnabled)
                            self.tableWidget.item(row, column).setBackground(QColor(200, 201, 204))

                self.flash_display_device_type()  # 进行类型筛选
        except Exception as e:
            sz_log_Error.error('add_device 异常: %s' % e)
            print(traceback.print_exc())

    #++++++++++++++++++++++++++++++ 子窗口显示 +++++++++++++++++++++++++++++++++++++++++
    def search_set(self):
        """搜寻网段设置"""
        try:
            self.search_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            self.search_window.center(position)
            self.search_window.Init_Window_Data(self.search_window.IP_data)
            self.search_window.show()
            self.setWindowOpacity(0.5)
        except Exception as e:
            sz_log_Error.error('search_set 异常: %s' % e)
            print(traceback.print_exc())


    def IP_show(self):
        """修改IP地址显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            if len(select_device_mac) > 1:
                self.IPmore_window.setWindowModality(Qt.ApplicationModal)
                # 获取主窗口左上角顶点坐标
                globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
                position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
                select_data = {}
                for mac in select_device_mac:
                    select_data[mac] = self.udp_data[mac]
                self.IPmore_window.device_data = select_data
                self.IPmore_window.window_updata()
                self.IPmore_window.center(position)
                self.IPmore_window.show()
            else:
                self.IPsingle_window.setWindowModality(Qt.ApplicationModal)
                globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
                position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
                select_data = {}
                for mac in select_device_mac:
                    select_data[mac] = self.udp_data[mac]
                self.IPsingle_window.device_data = select_data
                self.IPsingle_window.WindowDateInit()
                self.IPsingle_window.center(position)
                self.IPsingle_window.show()
        except Exception as e:
            sz_log_Error.error('IP_more_show 异常: %s' % e)
            print(traceback.print_exc())


    def Server_show(self):
        """服务器窗口显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            self.Server_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            select_data = {}
            for mac in select_device_mac:
                select_data[mac] = self.udp_data[mac]
            self.Server_window.device_data = select_data
            self.Server_window.window_updata()  # 界面数据更新
            self.Server_window.center(position)  # 子窗口定位
            self.Server_window.show()
        except Exception as e:
            sz_log_Error.error('Server_show 异常: %s' % e)
            print(traceback.print_exc())

    def Zigbee_show(self):
        """Zigbee窗口显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            self.Zigbee_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            select_data = {}
            for mac in select_device_mac:
                select_data[mac] = self.udp_data[mac]
            self.Zigbee_window.device_data = select_data
            self.Zigbee_window.window_updata()
            self.Zigbee_window.center(position)
            self.Zigbee_window.show()

        except Exception as e:
            sz_log_Error.error('Zigbee_show 异常: %s' % e)
            print(traceback.print_exc())


    def Updata_show(self):
        """固件升级窗口显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            self.Updata_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            select_data = {}
            for mac in select_device_mac:
                select_data[mac] = self.udp_data[mac]
            self.Updata_window.device_data = select_data
            self.Updata_window.window_updata()
            self.Updata_window.center(position)
            self.Updata_window.show()
        except Exception as e:
            sz_log_Error.error('Updata_window 异常: %s' % e)
            print(traceback.print_exc())

    def CheakTime_show(self):
        """校时窗口显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            self.CheakTime_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            select_data = {}
            for mac in select_device_mac:
                select_data[mac] = self.udp_data[mac]
            self.CheakTime_window.device_data = select_data
            self.CheakTime_window.window_updata()
            self.CheakTime_window.center(position)
            self.CheakTime_window.show()
        except Exception as e:
            sz_log_Error.error('CheakTime_window 异常: %s' % e)
            print(traceback.print_exc())

    def Reboot_show(self):
        """重启窗口显示"""
        try:
            select_device_mac = self.GET_select_device_mac()
            self.Reboot_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            select_data = {}
            for mac in select_device_mac:
                select_data[mac] = self.udp_data[mac]
            self.Reboot_window.device_data = select_data
            self.Reboot_window.window_updata()
            self.Reboot_window.center(position)

            self.Reboot_window.show()
        except Exception as e:
            sz_log_Error.error('Reboot_window 异常: %s' % e)
            print(traceback.print_exc())

    def version_show(self):
        """版本信息窗口显示"""
        try:
            self.version_window.setWindowModality(Qt.ApplicationModal)
            globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
            position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
            self.version_window.center(position)
            # self.Reboot_window.device_data['MAC地址'] = MAC
            self.version_window.show()
        except Exception as e:
            sz_log_Error.error('版本信息窗口显示 异常: %s' % e)
            print(traceback.print_exc())

    def Administrator_show(self):
        """管理员界面登录显示"""
        try:
            if self.Administrator_status == 0: # 没有进行管理员登录
                self.Administrator_window.setWindowModality(Qt.ApplicationModal)
                globalPos = self.mapToGlobal(QtCore.QPoint(0, 0))
                position = [globalPos.x(), globalPos.y(), self.width(), self.height()]
                self.Administrator_window.center(position)
                self.Administrator_window.show()
            else:
                self.Administrator_status = 0
                self.lineEdit_2.setPlaceholderText('请输入密码')
                self.pushButton_17.setText('管理员登录')
                self.pushButton_17.setStyleSheet('''
                            /*按钮普通态*/
                            QPushButton
                            {
                                /*字体为微软雅黑*/
                                font-family:Microsoft Yahei;
                                /*字体大小为20点*/
                                font-size:7pt;
                                /*字体颜色*/ 
                                color: rgb(21, 117, 212);
                                /*边框圆角半径为8像素*/ 
                                border-radius:2px;
                                width:65px;
                            }
                            /*按钮停留态*/
                            QPushButton:hover
                            {
                                /*字体颜色*/ 
                                color: rgb(255, 0, 0);
                            }
                            /*按钮按下态*/
                            QPushButton:pressed
                            {
                                /*左内边距为3像素，让按下时字向右移动3像素*/  
                                padding-left:3px;
                                /*上内边距为3像素，让按下时字向下移动3像素*/  
                                padding-top:3px;
                            }''')
        except Exception as e:
            sz_log_Error.error('管理员界面登录显示 异常: %s' % e)
            print(traceback.print_exc())

    #++++++++++++++++++++++++++++++++子界面反馈函数++++++++++++++++++++++++++++++++
    def Administrator_login_result(self, result):
        try:
            if result == 'success':
                self.Administrator_status = 1
            self.Administrator_window.lineEdit.setText('')  # 清除已经输入的密码
            self.lineEdit_2.setPlaceholderText('管理员无需输入密码')
            self.pushButton_17.setText('退出管理员登录')
            self.pushButton_17.setStyleSheet('''
            /*按钮普通态*/
            QPushButton
            {
                /*字体为微软雅黑*/
                font-family:Microsoft Yahei;
                /*字体大小为20点*/
                font-size:7pt;
                /*字体颜色*/ 
                color: rgb(255, 0, 0);
                /*边框圆角半径为8像素*/ 
                border-radius:2px;
                width:65px;
            }
            /*按钮停留态*/
            QPushButton:hover
            {
                /*字体颜色*/ 
                color: rgb(255, 0, 0);
            }
            /*按钮按下态*/
            QPushButton:pressed
            {
                /*左内边距为3像素，让按下时字向右移动3像素*/  
                padding-left:3px;
                /*上内边距为3像素，让按下时字向下移动3像素*/  
                padding-top:3px;
            }''')

        except Exception as e:
            print(traceback.print_exc())

    def feedback_change_ip_single(self):
        '''更改单个ip界面反馈函数'''
        try:
            if self.IPsingle_window.selectstate == 0:
                self.label_5.setStyleSheet('''''')

            else:
                self.label_5.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')

        except Exception as e:
            print(traceback.print_exc())

    def feedback_change_ip_more(self):
        '''更改多个IP界面反馈函数'''
        try:
            if self.IPmore_window.selectstate == 0:
                self.label_5.setStyleSheet('''''')
            else:
                self.label_5.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
        except Exception as e:
            print(traceback.print_exc())

    def feedback_change_server(self):
        '''修改服务器指向界面退出反馈函数'''
        try:
            if self.Server_window.selectstate == 0:
                self.label_6.setStyleSheet('''''')
            else:
                self.label_6.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
        except Exception as e:
            print(traceback.print_exc())

    def feedback_change_zigbee(self):
        '''修改zigbee界面退出反馈函数'''
        try:
            if self.Zigbee_window.selectstate == 0:
                self.label_7.setStyleSheet('''''')
            else:
                self.label_7.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
        except Exception as e:
            print(traceback.print_exc())

    def feedback_updata(self):
        '''固件升级界面退出反馈函数'''
        try:
            if self.Updata_window.selectstate == 0:
                self.pushButton_14.setEnabled(True)
                self.pushButton_15.setEnabled(True)
                self.pushButton_9.setEnabled(True)
                self.label_8.setStyleSheet('''''')
            else:
                self.pushButton_14.setEnabled(False)
                self.pushButton_15.setEnabled(False)
                self.pushButton_9.setEnabled(False)
                self.label_8.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
        except Exception as e:
            print(traceback.print_exc())

    def feedback_cheak_timing(self):
        '''校时界面退出反馈函数'''
        try:
            if self.CheakTime_window.selectstate == 0:
                self.label_9.setStyleSheet('''''')
            else:
                self.label_9.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
        except Exception as e:
            print(traceback.print_exc())


    def feedback_timing_reboot(self):
        '''定时重启界面反馈函数'''
        try:
            if self.Reboot_window.selectstate == 0:
                self.label_12.setStyleSheet('''''')
                self.pushButton_12.setEnabled(True)
                self.pushButton_14.setEnabled(True)
                self.pushButton_15.setEnabled(True)
            else:
                self.label_12.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
                self.pushButton_12.setEnabled(False)
                self.pushButton_14.setEnabled(False)
                self.pushButton_15.setEnabled(False)
        except Exception as e:
            print(traceback.print_exc())




    #++++++++++++++++++++++++++++++++数据处理函数++++++++++++++++++++++++++++++++
    def tableWidget_item_updata(self, row, column, text):
        '''表格单元格数据更新'''
        try:
            self.tableWidget.item(row, column).setText(text)
        except Exception as e:
            print(traceback.print_exc())

    def GET_select_device_mac(self):
        """ 获取选中设备的mac"""
        try:
            device_data = []
            row_num = self.tableWidget.rowCount()
            for row in range(row_num):
                if self.tableWidget_control_list[row][0].isChecked():
                    column = self.find_column_table('MAC地址')
                    device_data.append(self.tableWidget.item(row, column).text())
            return device_data
        except Exception as e:
            sz_log_Error.error('GET_select_device_mac 异常: %s' % e)
            print(traceback.print_exc())

    def GET_SELECTED_ALLDATA(self, mode=1):
        '''获取所有选中设备的信息'''
        try:
            device_data = {}
            row_num = self.tableWidget.rowCount() #表格行数
            column_num = self.tableWidget.columnCount() #表格列数
            i = 0
            if mode == 1:
                for row in range(row_num):#只获取选中的设备数据
                    if self.tableWidget_control_list[row][0].isChecked():
                        data = []
                        for column in range(column_num):
                            if column == 0:#跳过第0列
                                continue
                            if self.tableWidget.item(row, column) == None:
                                data.append('')
                            else:
                                data.append(self.tableWidget.item(row, column).text())
                        device_data[i] = data
                        i += 1
            else:
                for row in range(row_num):#获取所有的设备数据（包括隐藏）
                    data = []
                    for column in range(column_num):
                        if column == 0:#跳过第0列
                            continue
                        if self.tableWidget.item(row, column) == None:
                            data.append('')
                        else:
                            data.append(self.tableWidget.item(row, column).text())
                    device_data[i] = data
                    i += 1
            return device_data
        except Exception as e:
            print(traceback.print_exc())
            sz_log_Error.error('获取所有选中设备的信息 异常: %s' % e)

    def Export_tablewidget_data(self):
        '''导出设备信息到execl表格'''
        try:
            device_data = self.GET_SELECTED_ALLDATA()
            if len(device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未选择设备!')
                return
            fileName, ok = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", Export_path, "Text Files(*.xlsx)")
            list_header = []
            column_num = self.tableWidget.columnCount()
            for column in range(column_num):
                if column == 0:  # 跳过第0列
                    continue
                list_header.append(self.tableWidget.horizontalHeaderItem(column).text())
            if len(fileName) > 0:
                workbook = xlsxwriter.Workbook(fileName)  # 创建一个excel文件
                worksheet = workbook.add_worksheet(u'设备数据')  # 表名
                worksheet.set_column(0, len(list_header), 22)  # xlwt中是行和列(0第0行, lies_column设置多少列, 20宽度20像素)

                style = workbook.add_format({
                    # "fg_color": "white",  # 单元格的背景颜色
                    "bold": 1,  # 字体加粗
                    "align": "center",  # 对齐方式
                    "valign": "vcenter",  # 字体对齐方式
                    # "font_color": "red"  # 字体颜色
                })
                style2 = workbook.add_format({
                    "align": "center",  # 对齐方式
                    "valign": "vcenter",  # 字体对齐方式
                })
                for column in range(len(list_header)):  # 第一行添加自定义样式
                    worksheet.write(0, column, list_header[column], style)

                for row in range(len(device_data)):
                    for column in range(len(list_header)):  #添加内容和自定义样式
                        worksheet.write(row + 1, column, device_data[row][column], style2)
                workbook.close()
                # win32api.ShellExecute(None, 'open', fileName, None, None, 1)
        except Exception as e:
            sz_log_Error.error('导出设备信息到execl表格 异常: %s' % e)
            print(traceback.print_exc())

    def find_device_data(self, data, mode=1):
        """查找数据"""
        try:
            num = self.tableWidget.rowCount()
            if mode == 1:  # 查找设备的mac地址
                lable = self.find_column_table('MAC地址')
                if lable is None:
                    return None
                for x in range(num):
                    if self.tableWidget.item(x, lable).text() == data:
                        return x, lable
                return None, None
            elif mode == 2:  # 查找设备的IP地址
                lable_ip = self.find_column_table('设备IP地址')
                if lable_ip is None:
                    return None
                for x in range(num):
                    if self.tableWidget.item(x, lable_ip).text() == data:
                        return x, lable_ip
                return None, None
        except Exception as e:
            sz_log_Error.error('find_device_data 异常: %s' % e)
            print(traceback.print_exc())

    def tableWidget_search(self):
        '''表格搜索'''
        try:
            data = self.lineEdit.text()
            if data == '':
                return
            self.restore_tablewidget_color_Qtime_QtCore.emit() #复原表格颜色
            num = self.tableWidget.rowCount()

            lable = self.find_column_table('MAC地址')
            if lable is None:
                return None
            for row in range(num):
                if data in self.tableWidget.item(row, lable).text():
                    if data == self.tableWidget.item(row, lable).text():#精确查找
                        self.set_tablewidget_color_Qtime_QtCore.emit(row, lable)#背景变色
                        self.tableWidget.verticalScrollBar().setSliderPosition(row)#设备列表滚动条定位
                        return
                    else:#模糊查找
                        self.set_tablewidget_color_Qtime_QtCore.emit(row, lable)
                        # self.tableWidget.item(row, lable).setSelected(True)

            lable_ip = self.find_column_table('设备IP地址')
            if lable_ip is None:
                return None
            for row in range(num):
                if data in self.tableWidget.item(row, lable_ip).text():
                    if data == self.tableWidget.item(row, lable_ip).text():  # 精确查找
                        self.set_tablewidget_color_Qtime_QtCore.emit(row, lable_ip)  # 背景变色
                        self.tableWidget.verticalScrollBar().setSliderPosition(row)  # 设备列表滚动条定位

                        return
                    else:  # 模糊查找
                        self.set_tablewidget_color_Qtime_QtCore.emit(row, lable_ip)

        except Exception as e:
            print(traceback.print_exc())
            sz_log_Error.error('表格搜索 异常: %s' % e)

    def search_internet(self):
        '''双击IP进浏览器'''
        try:
            row_select = self.tableWidget.selectedItems()
            row = row_select[0].row()
            column_select = self.tableWidget.currentColumn()
            if self.tableWidget.horizontalHeaderItem(column_select).text() == '设备IP地址':
                text = self.tableWidget.item(row, column_select).text()#获取IP地址
                my_text = "http://" + text#合成访问连接
                QDesktopServices.openUrl(QUrl(my_text))#调用默认浏览器访问网站
        except Exception as e:
                print(traceback.print_exc())
                sz_log_Error.error('双击IP进浏览器 异常: %s' % e)

    def flash_tableWidget_data(self):
        """刷新网段设备"""
        try:
            for i in reversed(range(self.tableWidget.rowCount())):  # 清空表格
                self.delete_tableWidget_row(i)
            self.add_device(self.udp_data, 'online')  # 添加设备
            self.offline_marking()
            if self.udp_data != None:
                self.device_count = len(self.udp_data)
            else:
                self.device_count = 0
            self.lcdNumber.display(str(self.device_count))

        except Exception as e:
            sz_log_Error.error('flash_tableWidget_data 异常: %s' % e)
            print(traceback.print_exc())

    def flash_device(self):
        """刷新网段设备"""
        try:
            if len(self.search_window.IP_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未设置搜索网段!')
                return
            self.pushButton_2.setText('获取设备中')
            self.pushButton_2.setEnabled(False)
            self.Server_window.lastip = None
            self.Zigbee_window.lastip = None

            if self.search_window.IP_data['type'] == 'local':
                self.udp_same_network_scanning()

            elif self.search_window.IP_data['type'] == 'other':
                self.udp_other_network_scanning()
            self.pushButton_2.setText('刷新网段设备')
            self.pushButton_2.setEnabled(True)

        except Exception as e:
            sz_log_Error.error('flash_device 异常: %s' % e)
            print(traceback.print_exc())

    def udp_same_network_scanning(self):
        """ UDP同网段扫描网关 """
        try:
            local_netcard = '.'.join(get_local_ip().split('.')[0:3])
            if local_netcard:
                self.udp_data = udp_same_scanning(local_netcard)
                self.flash_tableWidget_data_Qtcore.emit()
            else:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未获取到电脑以太网卡,无法获取电脑ip地址,请检查电脑环境。')

        except Exception as e:
            sz_log_Error.error('udp_scanning_ip_mac 异常: %s' % e)
            print(traceback.print_exc())
            self.signal_Popup_Qtime_QtCore.emit('提示', '未扫描到设备')


    def udp_other_network_scanning(self):
        """ UDP 其他网段扫描网关 """
        try:
            com_4 = self.search_window.IP_data['net1_part4']
            com_3 = self.search_window.IP_data['net1_part3']
            com_2 = self.search_window.IP_data['net1_part2']
            com_1 = self.search_window.IP_data['net1_part1']

            com_8 = self.search_window.IP_data['net2_part4']
            com_7 = self.search_window.IP_data['net2_part3']
            com_6 = self.search_window.IP_data['net2_part2']
            com_5 = self.search_window.IP_data['net2_part1']

            if (com_4 == com_8) and (com_3 == com_7) and (int(com_2) <= int(com_6)) and (int(com_1) <= int(com_5)):
                com_mand_list = [(com_4 + '.' + com_3 + '.' + com_2 + '.' + com_1)
                    , (com_8 + '.' + com_7 + '.' + com_6 + '.' + com_5)]

                self.udp_data = print_ip_list(com_mand_list)
                self.flash_tableWidget_data_Qtcore.emit()
            else:
                com_mand_list = [(com_4 + '.' + com_3 + '.' + com_2 + '.' + com_1)
                    , (com_8 + '.' + com_7 + '.' + com_6 + '.' + com_5)]
                self.signal_Popup_Qtime_QtCore.emit('提示', '起始网段 >结束网段\n%s\n数据不合法' % com_mand_list)
        except Exception as e:
            sz_log_Error.error('udp_scanning_gw_ip_mac 异常: %s' % e)
            print(traceback.print_exc())
            self.signal_Popup_Qtime_QtCore.emit('提示', '未扫描到设备')
    ###############################################指令触发函数############################################


    def change_server_action_function(self, select_device_data, passwd, udp_client):
        '''服务器动作函数'''
        try:

            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_change_erver(mac, passwd, self.Server_window.SeverListData)
                send_data = aes_encrypt(send_data)
                # print(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据

        except Exception as e:
            print(traceback.print_exc())

    def change_Zigbee_action_function(self, select_device_data, passwd, udp_client):
        '''Zigbee修改动作函数'''
        try:
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                name = self.udp_data[mac]['bdinfo']
                channel = self.Zigbee_window.WINDOW_DATA['频点']
                pan_id = self.Zigbee_window.WINDOW_DATA['频点ID']
                send_data = random_change_zigbee(mac, passwd, name, channel, pan_id)
                send_data = aes_encrypt(send_data)
                # print(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据

        except Exception as e:
            print(traceback.print_exc())


    def restore_factory_action_function(self, select_device_data, passwd, udp_client):
        ''''恢复出厂设置动作函数'''
        try:
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_initialization(mac, passwd)
                send_data = aes_encrypt(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())

    def reboot_timing_action_function(self, select_device_data, passwd, udp_client):
        ''''定时重启指令动作函数'''
        try:
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_timing_reboot(mac, passwd, self.Reboot_window.restart_data)
                send_data = aes_encrypt(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())

    def restart_now_function(self, select_device_data, passwd, udp_client):
        ''''立即重启'''
        try:
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_reboot(mac, passwd)
                send_data = aes_encrypt(send_data)
                # print(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())

    def cheak_time_action_function(self, select_device_data, passwd, udp_client):
        ''''校时动作函数'''
        try:
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_cheak_timing(mac, passwd, self.CheakTime_window.Timing_data)
                send_data = aes_encrypt(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())

    def firmware_updata_action_function(self, select_device_data, passwd, udp_client):
        ''''固件升级动作函数'''
        try:
            #1、复制指定文件到程序内部文件夹
            path = copy_file(self.Updata_window.filename, r'.\bdinfo')
            if path == False:
                self.signal_Popup_Qtime_QtCore.emit('提示', '复制固件失败，请检查固件是否存在!')
                return
            else:
                # myname = socket.getfqdn(socket.gethostname())
                # ip = socket.gethostbyname(myname)
                ip = get_local_ip()
                print(ip)
                url = 'http://%s:8888%s' % (ip, path[1:])
                url = url.replace('\\', r'/')

                if os.path.isfile(path):
                    fp = open(path, 'rb')
                    contents = fp.read()
                    fp.close()
                    md5 = hashlib.md5(contents).hexdigest()
                    print(md5)
            for i in range(len(select_device_data)):
                mac = select_device_data[i][1]
                ip = self.udp_data[mac]['ipaddr']
                if int(self.udp_data[mac]['storage_size']) < os.path.getsize(path):
                    row, column = self.find_device_data(ip, mode=2)
                    if row != None and column != None:
                        self.set_error_device_table_color_Qtime.emit(row, column)
                        self.tableWidget.item(row, column).setToolTip(self.tableWidget.item(row, column).toolTip() + '内存不足(固件升级)\n')
                    continue
                ip_port = (ip, 8887)  # 网关的网段端口
                send_data = random_firmware_updata(mac, passwd, md5, url)
                send_data = aes_encrypt(send_data)
                udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())

    def change_network_info_action_function(self, select_device_data, passwd, udp_client):
        ''''修改网络配置'''
        try:
            if self.IPsingle_window.selectstate == 1:
                for i in range(len(select_device_data)):
                    mac = select_device_data[i][1]
                    ip = self.udp_data[mac]['ipaddr']
                    mode = self.udp_data[mac]['mode']
                    ip_port = (ip, 8887)  # 网关的网段端口
                    send_data = random_change_network_info(mac, passwd, mode, self.IPsingle_window.IPDATA)
                    send_data = aes_encrypt(send_data)
                    udp_client.sendto(send_data, ip_port)  # 发送数据
            elif self.IPmore_window.selectstate == 1:
                if self.IPmore_window.IPDATA['proto'] == 'static':
                    network_data = []
                    for card in range(int(self.IPmore_window.IPDATA['start_ip'][2]), int(self.IPmore_window.IPDATA['end_ip'][2]) + 1):
                        for last in range(int(self.IPmore_window.IPDATA['start_ip'][3]), int(self.IPmore_window.IPDATA['end_ip'][3]) + 1):
                            ip = '.'.join([self.IPmore_window.IPDATA['start_ip'][0], self.IPmore_window.IPDATA['start_ip'][1], str(card), str(last)])
                            network_data.append({
                                "proto": self.IPmore_window.IPDATA["proto"],
                                "ipaddr": ip,
                                "netmask": self.IPmore_window.IPDATA["netmask"],
                                "gateway": self.IPmore_window.IPDATA["gateway"],
                                "dns": self.IPmore_window.IPDATA["dns"],
                                "dns_flag": self.IPmore_window.IPDATA["dns_flag"]
                            })
                    for i in range(len(select_device_data)):
                        mac = select_device_data[i][1]
                        ip = self.udp_data[mac]['ipaddr']
                        mode = self.udp_data[mac]['mode']
                        ip_port = (ip, 8887)  # 网关的网段端口
                        send_data = random_change_network_info(mac, passwd, mode, network_data[i])
                        send_data = aes_encrypt(send_data)
                        udp_client.sendto(send_data, ip_port)  # 发送数据
                else:
                    for i in range(len(select_device_data)):
                        mac = select_device_data[i][1]
                        ip = self.udp_data[mac]['ipaddr']
                        mode = self.udp_data[mac]['mode']
                        ip_port = (ip, 8887)  # 网关的网段端口
                        send_data = random_change_network_info(mac, passwd, mode, self.IPmore_window.IPDATA)
                        send_data = aes_encrypt(send_data)
                        udp_client.sendto(send_data, ip_port)  # 发送数据
        except:
            udp_client.close()
            print(traceback.print_exc())


    def restore_factory_click_function(self):
        '''恢复出厂设置点击函数'''
        try:
            if self.restore_factory_state == 0:
                self.restore_factory_state = 1
                self.pushButton_12.setEnabled(False)
                self.pushButton_15.setEnabled(False)
                self.pushButton_9.setEnabled(False)
                self.label_10.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
            else:
                self.restore_factory_state = 0
                self.pushButton_12.setEnabled(True)
                self.pushButton_15.setEnabled(True)
                self.pushButton_9.setEnabled(True)
                self.label_10.setStyleSheet('''''')
        except Exception as e:
            print(traceback.print_exc())

    def restate_now_click_function(self):
        '''立即重启按键点击函数'''
        try:
            if self.reboot_now_state == 0:
                self.reboot_now_state = 1
                self.label_11.setStyleSheet('''image: url(:/png/shuncom_ico/png_ico/正确.png);''')
                self.pushButton_9.setEnabled(False)
                self.pushButton_12.setEnabled(False)
                self.pushButton_14.setEnabled(False)
            else:
                self.reboot_now_state = 0
                self.label_11.setStyleSheet('''''')
                self.pushButton_9.setEnabled(True)
                self.pushButton_12.setEnabled(True)
                self.pushButton_14.setEnabled(True)
        except Exception as e:
            print(traceback.print_exc())



    def order_recv_function(self, udp_client, time):
        '''指令接收函数'''
        try:
            udp_client.settimeout(time * 3)  # 获取套接字默认超时时间10秒
            while True:
                recvdata, addr = udp_client.recvfrom(1024)
                recvdata = aes_decrypt(recvdata)
                print(recvdata)
                recvdata['addr'] = addr

                if recvdata['function'] == "reboot":  # 立即重启
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(立即重启)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "cloud_config_write":  # 服务器指向
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(修改服务器指向)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "module_config_write":  # Zigbee主站
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(修改Zigbee主站)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "factory_data_reset":  # 恢复出厂设置
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(恢复出厂设置)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "auto_reboot":  # 网关定时重启
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(网关定时重启)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "sync_time":  # 网关校时
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(网关校时)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "firmware_update":  # 固件升级
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(固件升级)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)

                if recvdata['function'] == "wan_write":  # 修改网络配置
                    if recvdata['message'] != '成功':
                        row, column = self.find_device_data(addr[0], mode=2)
                        if row != None and column != None:
                            self.set_error_device_table_color_Qtime.emit(row, column)
                            action_result = recvdata['message'] + '(修改网络配置)' + '\n'
                            self.tableWidget.item(row, column).setToolTip(
                                self.tableWidget.item(row, column).toolTip() + action_result)
                    else:
                        row, column = self.find_device_data(recvdata['addr'][0], mode=2)
                        if row != None and column != None:
                            self.tablewidget_item_updata_Qtime_QtCore.emit(row, column, 'IP已修改，请重新扫描')
        except Exception as e:
            self.pushButton_2.setEnabled(True)
            self.pushButton_16.setEnabled(True)
            self.pushButton_16.setText('应用')
            udp_client.close()


    def order_action_function(self):
        '''指令动作函数'''
        try:
            select_device_data = self.GET_SELECTED_ALLDATA()
            if len(select_device_data) == 0:
                self.signal_Popup_Qtime_QtCore.emit('提示', '未选择设备')
                return

            if self.Administrator_status == 0:  # 非管理员模式
                passwd = self.lineEdit_2.text()
                if passwd == '':
                    self.signal_Popup_Qtime_QtCore.emit('提示', '请输入密码')
                    return
            else:  # 管理员模式
                passwd = 'shuncom'
            self.restore_tablewidget_color_Qtime_QtCore.emit()  # 恢复单元格颜色
            self.TableWidgetToolTipClear()  # 清除表格中所有提示信息
            # 进行二次确认
            if self.reboot_now_state == 1:  # 立即重启
                result = QMessageBox.information(self, '提示', '是否立即重启?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result != QMessageBox.Yes:
                    return
            self.pushButton_2.setEnabled(False)
            self.pushButton_16.setEnabled(False)
            self.pushButton_16.setText('下发指令中')

            udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_client.bind(('', 9999))  # 电脑ip和端口

            _thread.start_new_thread(self.order_recv_function, (udp_client, len(select_device_data)))
            if self.Server_window.selectstate == 1:  # 修改服务器指向
                self.change_server_action_function(select_device_data, passwd, udp_client)
            if self.Zigbee_window.selectstate == 1:  # 修改Zigbee主栈
                self.change_Zigbee_action_function(select_device_data, passwd, udp_client)
            if self.CheakTime_window.selectstate == 1:  # 校时
                self.cheak_time_action_function(select_device_data, passwd, udp_client)
            if self.IPsingle_window.selectstate == 1 or self.IPmore_window.selectstate == 1:  # 修改设备IP
                self.change_network_info_action_function(select_device_data, passwd, udp_client)
            if self.Updata_window.selectstate == 1:  # 固件升级
                self.firmware_updata_action_function(select_device_data, passwd, udp_client)
            if self.restore_factory_state == 1:  # 恢复出厂设置
                self.restore_factory_action_function(select_device_data, passwd, udp_client)
            if self.reboot_now_state == 1:  # 立即重启
                self.restart_now_function(select_device_data, passwd, udp_client)
            else:
                if self.Reboot_window.selectstate == 1:  # 定时重启
                    self.reboot_timing_action_function(select_device_data, passwd, udp_client)
            self.order_state_clear_func()  # 选中图标清除和选中状态清零

        except Exception as e:
            print(traceback.print_exc())


    def order_state_clear_func(self):
        '''指令选中清楚函数'''
        try:
            '''选中图标清除和选中状态清零'''
            self.label_5.setStyleSheet('''''')
            self.label_6.setStyleSheet('''''')
            self.label_7.setStyleSheet('''''')
            self.label_8.setStyleSheet('''''')
            self.label_9.setStyleSheet('''''')
            self.label_10.setStyleSheet('''''')
            self.label_11.setStyleSheet('''''')
            self.label_12.setStyleSheet('''''')
            self.IPsingle_window.selectstate = 0
            self.IPmore_window.selectstate = 0
            self.Server_window.selectstate = 0
            self.Zigbee_window.selectstate = 0
            self.Updata_window.selectstate = 0
            self.CheakTime_window.selectstate = 0
            self.restore_factory_state = 0
            self.reboot_now_state = 0
            self.Reboot_window.selectstate = 0
            '''按键使能打开'''
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.pushButton_12.setEnabled(True)
            self.pushButton_13.setEnabled(True)
            self.pushButton_14.setEnabled(True)
            self.pushButton_15.setEnabled(True)
            self.pushButton_9.setEnabled(True)

        except Exception as e:
            print(traceback.print_exc())

    def offline_marking(self):
        '''不在线设备标识'''
        try:
            # 将扫描到的设备添加到历史列表中
            if self.udp_data != None:
                device_key = list(self.udp_data.keys())
                for key in device_key:
                    self.device_history_list[key] = self.udp_data[key]
                # 把历史列表中的数据和实时列表中的数据进行对比，找出不在线的设备并整理
                history_device_key = list(self.device_history_list.keys())
                offline_list = {}
                for key in history_device_key:
                    if key not in self.udp_data:
                        offline_list[key] = self.device_history_list[key]
                # 显示历史设备
                self.add_device(offline_list, 'offline')
            else:
                # 显示历史设备
                self.add_device(self.device_history_list, 'offline')


        except Exception as e:
            print(traceback.print_exc())
    ################################################初始化函数#############################################
    def Init_Window_Data(self):
        '''初始化界面数据'''
        try:
            # #1、数据库数据导入
            # SqlData = sql_read('界面数据', '', mode=2)
            # if SqlData != None:
            #     RowNum = len(SqlData)
            #     self.device_count = RowNum
            #
            #     for row in range(RowNum):
            #         device_type = SqlData[row]['设备类别']  # 设备类别
            #         MAC = SqlData[row]['MAC地址']  # MAC地址
            #         IP = SqlData[row]['设备IP地址']  # IP地址
            #         Firmware_version = SqlData[row]['固件版本号']  # 固件版本
            #         Hardware_model = SqlData[row]['硬件型号']  # 硬件型号
            #         Connection_mode = SqlData[row]['连接方式']  # 连接方式
            #         http_port = SqlData[row]['HTTP端口']  # 连接方式
            #         netmask = SqlData[row]['子网掩码']  # 子网掩码
            #
            #         self.Add_tableWidget_row(MAC)  # 添加新行控件
            #
            #         lable_device_type = self.find_column_table('设备类别')
            #         if lable_device_type is not None:
            #             self.tableWidget.setItem(row, lable_device_type, QtWidgets.QTableWidgetItem(device_type))  # 设备类别
            #             self.tableWidget.item(row, lable_device_type).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_mac = self.find_column_table('MAC地址')
            #         if lable_mac is not None:
            #             self.tableWidget.setItem(row, lable_mac, QtWidgets.QTableWidgetItem(MAC))  # MAC地址
            #             self.tableWidget.item(row, lable_mac).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_ip = self.find_column_table('设备IP地址')
            #         if lable_ip is not None:
            #             self.tableWidget.setItem(row, lable_ip, QtWidgets.QTableWidgetItem(IP))  # IP地址
            #             self.tableWidget.item(row, lable_ip).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_ver = self.find_column_table('固件版本号')
            #         if lable_ver is not None:
            #             self.tableWidget.setItem(row, lable_ver, QtWidgets.QTableWidgetItem(Firmware_version))  # 固件版本
            #             self.tableWidget.item(row, lable_ver).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_HW = self.find_column_table('硬件型号')
            #         if lable_HW is not None:
            #             self.tableWidget.setItem(row, lable_HW, QtWidgets.QTableWidgetItem(Hardware_model))  # 硬件型号
            #             self.tableWidget.item(row, lable_HW).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_proto = self.find_column_table('连接方式')
            #         if lable_proto is not None:
            #             self.tableWidget.setItem(row, lable_proto, QtWidgets.QTableWidgetItem(Connection_mode))  # 连接方式
            #             self.tableWidget.item(row, lable_proto).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_http = self.find_column_table('HTTP端口')
            #         if lable_http is not None:
            #             self.tableWidget.setItem(row, lable_http, QtWidgets.QTableWidgetItem(http_port))  # HTTP端口
            #             self.tableWidget.item(row, lable_http).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         lable_netmask = self.find_column_table('子网掩码')
            #         if lable_netmask is not None:
            #             self.tableWidget.setItem(row, lable_netmask, QtWidgets.QTableWidgetItem(netmask))  # 子网掩码
            #             self.tableWidget.item(row, lable_netmask).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #2、配置列显示
            if config_tablewidget_column != '':
                self.tableWidget_column = json.loads(config_tablewidget_column)
                self.tableWidget_3_column_show()
                self.set_tablewidget_column_list()
                self.flash_tablewidget_column_list()
            #3、配置界面颜色
            if config_font_color != '':
                self.tableWidget.setStyleSheet("color:%s" % config_font_color)
                self.groupBox_5.setStyleSheet("color:%s" % config_font_color)
            #4、配置搜索网段界面
            if config_search_set_data != '':
                self.search_window.Init_Window_Data(json.loads(config_search_set_data))
        except Exception as e:
            print(traceback.print_exc())

    def Save_Window_Data(self):
        '''保存界面数据'''
        try:
            # #1、保存表格数据到数据库
            # sql_table_creat('界面数据')
            # sql_delete_data('界面数据', '', mode=2)
            # window_data = self.GET_SELECTED_ALLDATA(mode=2)
            # for row in range(len(window_data)):
            #     sql_write('界面数据', window_data[row])
            #2、保存列设置数据到配置文件
            config_init.set('CONFIG_SHUNCOM', 'tableWidget_column', json.dumps(self.tableWidget_column))
            #3、保存搜索网段设置数据
            config_init.set('CONFIG_SHUNCOM', 'search_set_data', json.dumps(self.search_window.IP_data))
            config_init.write(open("Config/Config.ini", "w", encoding='utf-8-sig'))
        except Exception as e:
            print(traceback.print_exc())



if __name__ == '__main__':
    pass
