#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员:周标华
# time: 2022-01-11 17:08
# 文件名称: shuncom_main_1.PY
# 开发工具: PyCharm
# Version: 1.0.0
"""
声明：
"""

import traceback
import threading
import win32api
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QToolButton, QMessageBox, QHeaderView, QPushButton, QComboBox,\
    QVBoxLayout, QCheckBox, QTableWidgetItem, QAbstractItemView,QColorDialog,QListView ,QGraphicsDropShadowEffect
from PyQt5.QtCore import QTranslator, QRegExp, Qt, QPoint  # ,QTimer
from PyQt5.QtGui import QRegExpValidator, QIcon, QFont, QColor, QBrush, QCursor,QPixmap, QPainter, \
    QFont  # ,QTextCursor,QPalette  # ,QIntValidator, QDoubleValidator
from PyQt5 import QtCore, QtWidgets, QtGui
from shuncom_module.shuncom_sql import *
from shuncom_module.shuncom_fun import *


###############################自定义模块#################################
from shuncom_ui.tool_main import Ui_MainWindow
from shuncom_module.shuncom_log_init import sz_log_Error, sz_log_record
from shuncom_module.shuncom_params_init import *


__version__ = '1.0.0'  # 版本信息
__V_date__ = '2022年1月14日'  # 编辑时间


class MainWindow_main_1(QtWidgets.QMainWindow, Ui_MainWindow):
    """ ui功能 """
    # 弹窗信号
    signal_Popup_Qtime_QtCore = QtCore.pyqtSignal(str, str)
    flash_table_number_Qtime_QtCore = QtCore.pyqtSignal()
    set_tablewidget_color_Qtime_QtCore = QtCore.pyqtSignal(int, int)
    set_error_device_table_color_Qtime = QtCore.pyqtSignal(int, int)
    restore_tablewidget_color_Qtime_QtCore = QtCore.pyqtSignal()
    tablewidget_item_updata_Qtime_QtCore = QtCore.pyqtSignal(int, int, str)

    def __init__(self):
        super(MainWindow_main_1, self).__init__()
        self.trans = QTranslator()
        self.VerSectionClicked_on_off = 0  # 复选框全选标志位
        self.tableWidget_control_list = []  # 每行控件列表
        self.tableWidget_column = []  # 设备显示列的列表
        self.device_history_list = {}  # 历史设备里列表
        self.column_list = {'#': 0, '设备类别': 1, 'MAC地址': 2, '固件版本号': 3, '硬件型号': 4, '连接方式': 5, '设备IP地址': 6,
                    'HTTP端口': 7, '子网掩码': 8, 'SZIOT服务器IP地址:端口': 9, 'SZTT服务器IP地址:端口': 10, 'MQTT服务器IP地址:端口': 11, 'Zigbee频点': 12, 'Zigbee频点ID': 13}
        self.device_count = 0   # 设备数量
        self.reboot_now_state = 0  # 立即重启选择状态
        self.restore_factory_state = 0  # 恢复出厂设置选择状态
        self.Administrator_status = 0   # 管理员状态 1为已登录

    ##################################################右键菜单函数################################################

    def cheak_list_time_data_right(self, event):
        '''查看上次退出时的数据'''
        try:
            if event.text() == '查看上次退出时数据':
                sql_open()
        except Exception as e:
            sz_log_Error.error('查看上一次退出时的数据 异常: %s' % e)
            print(traceback.print_exc())  # 准确定位哪一行出问题

    def recovery_list_time_data_right(self, event):
        '''恢复上次退出时的数据'''
        try:
            if event.text() == '恢复上次退出时数据':
                pass
        except Exception as e:
            sz_log_Error.error('恢复上次退出时的数据 异常: %s' % e)
            print(traceback.print_exc())  # 准确定位哪一行出问题

    def delete_row_right(self, event):
        """删除"""
        try:
            if event.text() == '删除':
                indexs = self.tableWidget.selectionModel().selection().indexes()
                if len(indexs) > 0:
                    # 取第一行
                    index = indexs[0]
                    self.delete_tableWidget_row(index.row())
        except Exception as e:
            sz_log_Error.error('delete_row_right 异常: %s' % e)
            print(traceback.print_exc())  # 准确定位哪一行出问题


    def tableWidget_right_Menu(self):
        """# 鼠标右键菜单功能"""
        try:
            popMenu = QMenu()  # 创建右键菜单对象
            popMenu.addAction(QAction(QIcon(':/png/shuncom_ico/png_ico/删除4.png'), u'删除', self))  # 添加菜单可执行选项
            # popMenu.addAction(QAction(QIcon(':/png/shuncom_ico/png_ico2/show.png'), u'查看上次退出时数据', self))  # 添加菜单可执行选项
            # popMenu.addAction(QAction(QIcon(':/png/shuncom_ico/png_ico/恢复.png'), u'恢复上次退出时数据', self))  # 添加菜单可执行选项
            popMenu.triggered[QAction].connect(self.delete_row_right)  # 绑定显示具体方案信息函数
            # popMenu.triggered[QAction].connect(self.cheak_list_time_data_right)  # 绑定显示具体方案信息函数
            # popMenu.triggered[QAction].connect(self.delete_row_right)  # 绑定显示具体方案信息函数
            popMenu.exec_(QCursor.pos())
        except Exception as e:
            sz_log_Error.error('tableWidget_right_Menu 异常: %s' % e)
            print(traceback.print_exc())  # 准确定位哪一行出问题

    ##################################################其他UI界面函数################################################
    def Add_tableWidget_row(self, row):
        """新增一行"""
        try:
            control_list = []
            self.tableWidget_control_list.append(control_list)
            self.Add_checkbox_to_tableWidget(row)  # 添加一个复选框
            self.tableWidget.setRowHeight(row, 40)

        except Exception as e:
            sz_log_Error.error('Add_tableWidget_row 异常: %s' % e)
            print(traceback.print_exc())

    def delete_devices(self):
        """删除按钮"""
        try:
            num = self.tableWidget.rowCount()
            column = self.find_column_table('MAC地址')
            for row in reversed(range(num)):  # 倒序删除
                if self.tableWidget_control_list[row][0].isChecked():
                    self.device_history_list.pop(self.tableWidget.item(row, column).text())  # 删除历史记录
                    self.tableWidget.removeRow(row)  # 通过index的row()操作得到行数进行删除
                    self.tableWidget_control_list.pop(row)  # 删除对应行的控件
            self.flash_table_number_Qtime_QtCore.emit()
            self.tableWidget.horizontalHeaderItem(0).setIcon(QtGui.QIcon(":/png/shuncom_ico/png_ico2/复选框.png"))
        except Exception as e:
            sz_log_Error.error('delete_devices 异常: %s' % e)
            print(traceback.print_exc())

    def FlashNumber(self):
        '''更新序号'''
        try:
            rownum = self.tableWidget.rowCount()
            for row in range(rownum):
                self.tableWidget.item(row, 0).setText(str(row))
        except Exception as e:
            print(traceback.print_exc())



    def delete_tableWidget_row(self, data):
        """删除一行"""
        try:
            row = None
            if type(data) == int:
                row = data
            elif type(data) == str:
                row = self.find_device_data(data, mode=1)
            if row is None:
                return
            self.tableWidget.removeRow(row)  # 通过index的row()操作得到行数进行删除
            self.tableWidget_control_list.pop(row)  # 删除对应行的控件
            self.device_count -= 1
            self.flash_table_number_Qtime_QtCore.emit()  # 刷新表格序号

        except Exception as e:
            sz_log_Error.error('delete_tableWidget_row 异常: %s' % e)
            print(traceback.print_exc())


    def Add_checkbox_to_tableWidget(self, row):
        """添加复选框到列表"""
        try:
            cbox = QCheckBox()
            cbox.setText('')
            # 1.实例化一个新布局
            hLayout = QtWidgets.QHBoxLayout()
            # 2.在布局里添加checkBox
            hLayout.addWidget(cbox)
            # 3.在布局里居中放置checkbox1
            hLayout.setAlignment(cbox, Qt.AlignCenter)
            # 4.实例化一个QWidget（控件）
            widget = QtWidgets.QWidget()
            # 5.在QWidget放置布局
            widget.setLayout(hLayout)
            # 6.在tableWidget1放置widget
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row)))
            self.tableWidget.setCellWidget(row, 0, widget)
            self.tableWidget.item(row, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)#设置单元格对齐分式为水平右对齐，垂直居中对齐
            self.tableWidget_control_list[row].append(cbox)
        except Exception as e:
            sz_log_Error.error('Add_checkbox_to_tableWidget 异常: %s' % e)
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

    def SET_UI_QSS(self):
        """ 加载列表设置 """
        try:
            #######################################设置表格标头样式######################################
            self.tableWidget.setShowGrid(False)
            # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            '''列设置列表'''
            self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # self.tableWidget_3.horizontalHeader().setStyleSheet(
            #     '''QHeaderView::section{background:rgba(230,230,230,0)}''')
            '''设备列表'''
            # self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)#第0列自适应
            self.tableWidget.setColumnWidth(0, 60)   #设置复选框宽度
            self.tableWidget.setColumnWidth(2, 140)  # 设置mac地址列宽
            self.tableWidget.setColumnWidth(9, 180)  # 设置SZIOT服务器IP地址:端口列宽
            self.tableWidget.setColumnWidth(10, 180)  # 设置SZTT服务器IP地址:端口列宽
            self.tableWidget.setColumnWidth(11, 180)  # 设置MQTT服务器IP地址:端口列宽

            # self.tableWidget.setAlternatingRowColors(True)  # 设置表格为斑马灰白样式
            # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选择
            # self.tableWidget.horizontalHeader().setStyleSheet(
            #     '''QHeaderView::section{background:rgba(230,230,230,0)}''')
            self.tableWidget.horizontalScrollBar().setStyleSheet(horizontalScrollBarStyle)#设置水平滚动条样式
            self.tableWidget.verticalScrollBar().setStyleSheet(verticalScrollBarStyle)#设置垂直滚动条样式
            self.comboBox.setView(QListView())
            self.comboBox.setMaxVisibleItems(5)

            # self.tableWidget.verticalScrollBar().valueChanged.connect(lambda : self.tableWidget_2.verticalScrollBar().setValue(self.tableWidget.verticalScrollBar().value()))#表1关联更改表2的滚动条

            self.tableWidget.verticalHeader().setVisible(False)     # 取消列标题
            #######################################其他按键#######################################
            '''阴影设置'''
            self.add_shadow(self.pushButton_3)
            self.add_shadow(self.pushButton_4)
            self.add_shadow(self.pushButton_5)
            self.add_shadow(self.pushButton_6, value=10)
            self.add_shadow(self.pushButton_7, value=10)
            self.add_shadow(self.pushButton_8, value=10)
            self.add_shadow(self.pushButton_9, value=10)
            self.add_shadow(self.pushButton_11)
            self.add_shadow(self.pushButton_12, value=10)
            self.add_shadow(self.pushButton_13, value=10)
            self.add_shadow(self.pushButton_14, value=10)
            self.add_shadow(self.pushButton_15, value=10)
            self.add_shadow(self.tableWidget_3, value=10)

            self.add_shadow_white(self.pushButton)
            # self.add_shadow_white(self.comboBox)
            self.add_shadow(self.lineEdit_2)

            self.add_shadow(self.groupBox)
            self.add_shadow(self.groupBox_7, value=10)
            self.add_shadow_white(self.groupBox_17)
        except Exception as e:
            sz_log_Error.error('SET_UI_QSS 异常: %s' % e)
            print(traceback.print_exc())

    def TableWidgetToolTipClear(self):
        '''表格提示清除'''
        try:
            rownum = self.tableWidget.rowCount()
            for row in range(rownum):
                    self.tableWidget.item(row, 6).setToolTip('')
        except Exception as e:
            print(traceback.print_exc())

    def VerSectionClicked(self, index):
        """表头全选反选切换"""
        try:
            if index == 0 and self.VerSectionClicked_on_off == 0:
                self.tableWidget.horizontalHeaderItem(0).setIcon(
                    QtGui.QIcon(":/png/shuncom_ico/png_ico2/复选框-选中.png"))
                index = (int(self.tableWidget.rowCount()))  # 当前多少行
                for x in range(index):
                    self.tableWidget_control_list[x][0].setChecked(True)
                self.VerSectionClicked_on_off = 1
            elif index == 0 and self.VerSectionClicked_on_off == 1:
                self.tableWidget.horizontalHeaderItem(0).setIcon(QtGui.QIcon(":/png/shuncom_ico/png_ico2/复选框.png"))
                index = (int(self.tableWidget.rowCount()))
                for x in range(index):
                    self.tableWidget_control_list[x][0].setChecked(False)
                self.VerSectionClicked_on_off = 0
        except Exception as e:
            sz_log_Error.error('全选反选切换VerSectionClicked 异常: %s' % e)
            print(traceback.print_exc())

    def VerSectionClicked_list(self, index):
        """表头全选反选切换"""
        try:
            if index == 0 and self.VerSectionClicked_on_off == 0:
                self.tableWidget_3.horizontalHeaderItem(0).setIcon(
                    QtGui.QIcon(":/png/shuncom_ico/png_ico2/复选框-选中.png"))
                index = (int(self.tableWidget_3.rowCount()))  # 当前多少行
                for x in range(index):
                    if x == 0:
                        continue
                    self.tableWidget_3.item(x, 0).setCheckState(2)
                self.VerSectionClicked_on_off = 1
            elif index == 0 and self.VerSectionClicked_on_off == 1:
                self.tableWidget_3.horizontalHeaderItem(0).setIcon(
                    QtGui.QIcon(":/png/shuncom_ico/png_ico2/复选框.png"))
                index = (int(self.tableWidget_3.rowCount()))
                for x in range(index):
                    if x == 0:
                        continue
                    self.tableWidget_3.item(x, 0).setCheckState(0)
                self.VerSectionClicked_on_off = 0
        except Exception as e:
            sz_log_Error.error('全选反选切换VerSectionClicked 异常: %s' % e)
            print(traceback.print_exc())

    def set_select_tablewidget_color(self, row, column):
        '''设置选中单元格颜色'''
        try:
            # 字体颜色（白色）
            self.tableWidget.item(row, column).setForeground(QBrush(QColor(255, 255, 255)))
            # 背景颜色（湛蓝）
            self.tableWidget.item(row, column).setBackground(QBrush(QColor(0, 120, 215)))
        except Exception as e:
            print(traceback.print_exc())

    def set_error_device_table_color(self, row, column):
        '''设置指令请求出错的单元格设备颜色'''
        try:
            # 字体颜色（红色）
            self.tableWidget.item(row, column).setForeground(QBrush(QColor(255, 0, 0)))
            # 背景颜色（白色）
            self.tableWidget.item(row, column).setBackground(QBrush(QColor(255, 255, 255)))
        except Exception as e:
            print(traceback.print_exc())

    def hex2dec(self, string_num):
        """16进制转10进制 """
        return str(int(string_num.upper(), 16))

    def restore_tablewidget_color(self):
        '''复原单元格的颜色'''
        try:
            lable = self.find_column_table('MAC地址')
            lable_ip = self.find_column_table('设备IP地址')
            config_font_color = config_init.get('FONT_COLOR', 'config_font_color')
            if config_font_color == '':
                config_font_color = '#000000'
            red = int(self.hex2dec(config_font_color[1:3]))
            greed = int(self.hex2dec(config_font_color[3:5]))
            blue = int(self.hex2dec(config_font_color[5:7]))
            if (lable is None) and (lable_ip is None):
                return None
            rownum = self.tableWidget.rowCount()
            for row in range(rownum):
                if self.tableWidget.item(row, lable).flags() != self.tableWidget.item(row, lable).flags() & ~Qt.ItemIsEnabled:
                    # 字体颜色（自定义颜色）
                    self.tableWidget.item(row, lable).setForeground(QBrush(QColor(red, greed, blue)))
                    # 字体颜色（自定义颜色）
                    self.tableWidget.item(row, lable_ip).setForeground(QBrush(QColor(red, greed, blue)))

                    # 背景颜色（白色）
                    self.tableWidget.item(row, lable).setBackground(QBrush(QColor(255, 255, 255)))
                    # 背景颜色（白色）
                    self.tableWidget.item(row, lable_ip).setBackground(QBrush(QColor(255, 255, 255)))

        except Exception as e:
            print(traceback.print_exc())

    def SHOW_CLOSE_groupBox_7(self):
        """关闭、显示更多操作界面"""
        try:
            if self.groupBox_7.isHidden():
                self.groupBox_7.show()
                self.pushButton_11.setStyleSheet(QPushButtoStyle1)
                # self.pushButton_11.setIcon(QIcon(':/png/shuncom_ico/png_ico/右箭头.png'))
            else:
                self.groupBox_7.close()
                self.pushButton_11.setStyleSheet(QPushButtoStyle2)
                # self.pushButton_11.setIcon(QIcon(':/png/shuncom_ico/png_ico/左箭头.png'))
        except Exception as e:
            sz_log_Error.error('SHOW_CLOSE_groupBox 异常: %s' % e)
            print(traceback.print_exc())

    def SHOW_CLOSE_tableWidget_3(self):
        """关闭、显示更多列设置界面"""
        try:
            if self.tableWidget_3.isHidden():
                self.tableWidget_3.show()
            else:
                self.tableWidget_3.close()
                self.flash_tablewidget_column_list()
                self.tableWidget_3_column_show()
        except Exception as e:
            sz_log_Error.error('SHOW_CLOSE_tableWidget_3 异常: %s' % e)
            print(traceback.print_exc())

    def set_tablewidget_column_list(self):
        '''设置界面列显示勾选框'''
        try:
            row_num = self.tableWidget_3.rowCount()
            for row in range(row_num):
                if self.tableWidget_3.item(row, 0).text() not in self.tableWidget_column:
                    self.tableWidget_3.item(row, 0).setCheckState(0)

        except Exception as e:
            print(traceback.print_exc())

    def flash_tablewidget_column_list(self):
        '''刷新显示列勾选列表'''
        try:
            num = self.tableWidget_3.rowCount()
            self.tableWidget_column.clear()
            self.tableWidget_column.append('#')
            for row in range(num):
                if row == 0:
                    continue
                if self.tableWidget_3.item(row, 0).checkState() == 2:
                    self.tableWidget_column.append(self.tableWidget_3.item(row, 0).text())
        except Exception as e:
            sz_log_Error.error('刷新显示列勾选列表 异常: %s' % e)
            print(traceback.print_exc())

    def about(self):
        """# 关于"""
        QtWidgets.QMessageBox.about(self,
                                    "软件版本：V%s" % __version__,
                                    "<html><head/><body><p><span style=\" color:#ff0000;\">"
                                    "时间：%s<br/>"
                                    "公司：上海顺舟智能科技股份有限公司<br/>"
                                    "官网：<a href ='http://www.shuncom.com'>www.shuncom.com<br/></a>"
                                    "</span></p></body></html>" % __V_date__,
                                    )

    def tableWidget_3_column_show(self):
        """ 设置列表中的隐藏显示状态 # 当一列被隐藏后，其他列的列号不变"""
        try:
            # print(self.tableWidget_column)
            for column in reversed(range(self.tableWidget.columnCount())):
                if self.tableWidget.horizontalHeaderItem(column).text() in self.tableWidget_column:
                    self.tableWidget.setColumnHidden(column, False)  # 显示某一行
                else:
                    self.tableWidget.setColumnHidden(column, True)  # 隐藏某一行
        except Exception as e:
            sz_log_Error.error('tableWidget_3_column_show 异常: %s' % e)
            print(traceback.print_exc())

    def shuncom_set_font_color(self):
        """ 设置字体颜色 """
        try:
            col = QColorDialog.getColor()
            if col.isValid():
                col_c = col.name()
                self.tableWidget.setStyleSheet("color:%s" % col_c)
                self.groupBox_5.setStyleSheet("color:%s" % col_c)
                config_init.set('FONT_COLOR', 'config_font_color', col_c)
                config_init.write(open("Config/Config.ini", "w", encoding='utf-8-sig'))
        except Exception as Error:
            print('shuncom_set_font_color异常:', Error)
            sz_log_Error.error('shuncom_set_font_color异常:%s' % Error)

    def signal_Popup(self, newtypes, news):
        """ 弹窗提示功能 """
        try:
            if newtypes == '警告':
                QMessageBox.warning(self, '警告', news)
            if newtypes == '提示':
                QMessageBox.information(self, '提示', news)
            if newtypes == '危险':
                QMessageBox.ctitical(self, '危险', news)
            if newtypes == '问答':
                result = QMessageBox.question(self, '问答', news)
                print(result)
            if newtypes == '关于':
                QMessageBox.about(self, '关于', news)
        except Exception as e:
            sz_log_Error.error('signal_Popup异常:%s' % e)
            print(traceback.print_exc())



    def en_translation(self):
        """ 语言翻译 英语 """
        self.en_zn_state = 0
        self.trans.load("shuncom_ico\shuncom_en.qm")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        # 重新翻译界面
        self.retranslateUi(self)
        config_init.set("FONT_COLOR", "config_en_zn_on_off", '0')
        config_init.write(open("Config/Config.ini", "w", encoding='utf-8-sig'))

        translator = QTranslator(_app)
        if translator.load('shuncom_ico\qtbase_en.qm'):
            _app.installTranslator(translator)

    def zc_translation(self):
        """ 语言翻译 中文 """
        self.en_zn_state = 1
        self.trans.load("shuncom_ui\shuncom_zh_cn.qm")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        config_init.set("FONT_COLOR", "config_en_zn_on_off", '1')
        config_init.write(open("Config/Config.ini", "w", encoding='utf-8-sig'))

        translator = QTranslator(_app)
        if translator.load('shuncom_ico\qtbase_zh_CN.qm'):
            _app.installTranslator(translator)

    def set_en_zh_ui(self):
        """ 加载设置语言记录 """
        if config_en_zn_on_off == '1':
            self.en_zn_on_off = 1
            self.trans.load("shuncom_ui\shuncom_zh_cn.qm")
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
            translator = QTranslator(_app)
            if translator.load('shuncom_ico\qtbase_zh_CN.qm'):
                _app.installTranslator(translator)
        else:
            self.en_zn_on_off = 0
            self.trans.load("shuncom_ico\shuncom_en.qm")
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            # 重新翻译界面
            self.retranslateUi(self)



if __name__ == '__main__':
    pass
