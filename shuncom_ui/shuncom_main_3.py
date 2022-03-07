#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员:王灋權
# time: 2022-01-19 21:07
# 文件名称: shuncom_main.PY
# 开发工具: PyCharm
# Version: 1.0.0
"""
声明：加载重写窗口框架
"""
import traceback
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint,QTranslator
from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction, QWidget,QPushButton, QVBoxLayout,\
    QApplication,QHBoxLayout, QLabel, QSpacerItem, QSizePolicy,QMessageBox

#++++++++++++++++++++++++ 导入自定义包文件+++++++++++++++++++++++++++++++++++++
from shuncom_ui.shuncom_main_2 import ShuncomWidget
from shuncom_ui.tool_main import Ui_MainWindow
from shuncom_module.shuncom_log_init import sz_log_Error
from shuncom_ui.window_son.version_information_ui.version_information import version_info
global son_window


class TitleBar(QWidget, Ui_MainWindow):
    """ 标题栏 """
    # 窗口最小化信号
    windowMinimumed = QtCore.pyqtSignal()
    # 窗口最大化信号
    windowMaximumed = QtCore.pyqtSignal()
    # 窗口还原信号
    windowNormaled = QtCore.pyqtSignal()
    # 窗口关闭信号
    windowClosed = QtCore.pyqtSignal()
    # 窗口移动
    windowMoved = QtCore.pyqtSignal(QPoint)
    # 关于信号
    about_QtCore =  QtCore.pyqtSignal()
    # 设置语言,字体颜色信号
    set_language_QtCore = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        self.buttonMaximum_state = 0  # 最大化最小化状态
        self.en_zn_state = 1          # 1 中文简体，0 英文


        # 支持qss设置背景
        self.setAttribute(Qt.WA_StyledBackground)
        self.mPos = None
        self.iconSize = 20  # 图标的默认大小

        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 布局
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 窗口图标
        self.iconLabel = QLabel(self)
        self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)

        # 窗口标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        self.titleLabel.setStyleSheet("color: rgb(255, 255, 255);")
        layout.addWidget(self.titleLabel)

        # 中间伸缩条
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 利用Webdings字体来显示图标
        font = self.font() or QFont()
        font.setFamily('Webdings')

        menu = QMenu()  # 字体设置一个菜单对象
        self.typeface_pushbutton = QPushButton(font=font, objectName='typeface_pushbutton')
        typeface_icon = QtGui.QIcon()
        typeface_icon.addPixmap(QtGui.QPixmap(":/png/shuncom_ico/png_ico/字体1.png"))
        self.typeface_pushbutton.setIcon(typeface_icon)
        self.typeface_pushbutton.setFlat(True)
        self.typeface_pushbutton.setMenu(menu)  # 为按钮设置菜单
        self.typeface_pushbutton.setStyleSheet(" QPushButton::menu-indicator{image:none;} ")  # 取消显示向下箭头
        # toolButton.setStyleSheet( " QToolButton::menu-indicator{image:none;} " )  # 取消显示向下箭头

        menu.setStyleSheet("""
                   QMenu
                   {background-color:qlineargradient(
                   x1: 0, y1: 0, x2: 0.7, y2: 0.7,stop: 0.5 :rgb(81,72,65),stop:1 white);}
                   QMenu::item:selected
                   {background-color: rgb(246, 134, 86);}
               """)

        # # 设置字体颜色,切换语言
        # self.menu = menu     # menu 对象公有化
        # # self.add_menu()      # 添加子菜单栏
        # menu.addSeparator()  # 增加分割线分割开来
        # menu_about = QAction(QIcon(':/png/shuncom_ico/png_ico2/字体颜色.png'), "设置字体颜色", menu)
        # menu.addAction(menu_about)
        # layout.addWidget(self.typeface_pushbutton)
        # menu_about.triggered.connect(self.set_language_QtCore.emit)  # 设置字体颜色信号

        # 关于
        self.about_pushbutton = QPushButton(clicked=self.about_QtCore.emit, font=font, objectName='about_pushbutton')
        about_icon = QtGui.QIcon()
        about_icon.addPixmap(QtGui.QPixmap(":/png/shuncom_ico/png_ico/关于1.png"))
        self.about_pushbutton.setIcon(about_icon)
        layout.addWidget(self.about_pushbutton)

        # 最小化按钮
        self.buttonMinimum = QPushButton(clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
        Minimum_icon = QtGui.QIcon()
        Minimum_icon.addPixmap(QtGui.QPixmap(":/png/shuncom_ico/png_ico/最小化1.png"))
        self.buttonMinimum.setIcon(Minimum_icon)
        layout.addWidget(self.buttonMinimum)

        # 最大化/还原按钮
        self.buttonMaximum = QPushButton(self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
        Maximum_icon = QtGui.QIcon()
        Maximum_icon.addPixmap(QtGui.QPixmap(":/png/shuncom_ico/png_ico/最大化1.png"))
        self.buttonMaximum.setIcon(Maximum_icon)
        layout.addWidget(self.buttonMaximum)

        # 关闭按钮
        self.buttonClose = QPushButton(self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
        Close_icon = QtGui.QIcon()
        Close_icon.addPixmap(QtGui.QPixmap(":/png/shuncom_ico/png_ico/关闭1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonClose.setIcon(Close_icon)
        layout.addWidget(self.buttonClose)

        # 初始高度
        self.setHeight()



    def add_menu(self):
        """ 子菜单栏 """
        global son_window
        try:
            Sub_menu = QMenu('切换语言', self.menu)
            act1 = QAction(QIcon(':/png/shuncom_ico/png_ico2/中文.png'), "简体中文", Sub_menu)
            act1.triggered.connect(lambda: son_window.zc_translation())
            Sub_menu.addAction(act1)
            act2 = QAction(QIcon(':/png/shuncom_ico/png_ico2/英语.png'), "English", Sub_menu)
            act2.triggered.connect(lambda: son_window.en_translation())
            Sub_menu.addAction(act2)

            self.menu.addMenu(Sub_menu)
        except Exception as e:
            sz_log_Error.error("子菜单栏异常 %s " % e)
            print("子菜单栏异常 %s " % e)



    def showMaximized(self):
        """最大化 还原"""
        if self.buttonMaximum_state == 0:
            # 最大化
            self.buttonMaximum_state = 1
            self.windowMaximumed.emit()
        else:
            # 还原
            self.buttonMaximum_state = 0
            self.windowNormaled.emit()


    def setHeight(self, height=35):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)
        self.about_pushbutton.setMinimumSize(height, height)
        self.about_pushbutton.setMaximumSize(height, height)
        self.typeface_pushbutton.setMinimumSize(height, height)
        self.typeface_pushbutton.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """设置图标 显示"""
        #self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))
        pass

    def setIconSize(self, size):
        """设置图标大小"""
        self.iconSize = size

    def enterEvent(self, event):
        """ 输入事件 """
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        """ 鼠标双击事件 """
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """ 鼠标点击事件 """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        self.mPos = None
        event.accept()


    def mouseMoveEvent(self, event):
        """鼠标移动事件"""

        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))

        event.accept()



#++++++++++++++++++++++++++++ 无框架窗口 ++++++++++++++++++++++++++++++++++++++++++++++++
# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class shuncom_FramelessWindow(QWidget):
    """ 无框架窗口 """
    Margins = 5  # 四周边距

    def __init__(self, *args, **kwargs):
        super(shuncom_FramelessWindow, self).__init__(*args, **kwargs)
        self._pressed = False
        self.Direction = None
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        # 鼠标跟踪
        self.setMouseTracking(True)
        # 布局
        layout = QVBoxLayout(self, spacing=0)
        # 预留边界用于实现无边框窗口调整大小
        layout.setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        # 标题栏
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)
        # 信号槽
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.shuncom_close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)
        self.titleBar.about_QtCore.connect(self.about)
        self.titleBar.set_language_QtCore.connect(self.typeface_function)


    def setTitleBarHeight(self, height=35):
        """设置标题栏高度"""
        self.titleBar.setHeight(height)

    def setIconSize(self, size):
        """设置图标的大小"""
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """设置自己的控件"""
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        """ # 最大化或者全屏则不允许移动 """
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(shuncom_FramelessWindow, self).move(pos)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        super(shuncom_FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        super(shuncom_FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(shuncom_FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super(shuncom_FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        global son_window
        super(shuncom_FramelessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True


    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""

        super(shuncom_FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None


    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        try:
            super(shuncom_FramelessWindow, self).mouseMoveEvent(event)
            pos = event.pos()
            xPos, yPos = pos.x(), pos.y()
            wm, hm = self.width() - self.Margins, self.height() - self.Margins
            if self.isMaximized() or self.isFullScreen():
                self.Direction = None
                self.setCursor(Qt.ArrowCursor)
                return
            if event.buttons() == Qt.LeftButton and self._pressed:
                self._resizeWidget(pos)
                return
            if xPos <= self.Margins and yPos <= self.Margins:
                # 左上角
                self.Direction = LeftTop
                self.setCursor(Qt.SizeFDiagCursor)
            elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
                # 右下角
                self.Direction = RightBottom
                self.setCursor(Qt.SizeFDiagCursor)
            elif wm <= xPos and yPos <= self.Margins:
                # 右上角
                self.Direction = RightTop
                self.setCursor(Qt.SizeBDiagCursor)
            elif xPos <= self.Margins and hm <= yPos:
                # 左下角
                self.Direction = LeftBottom
                self.setCursor(Qt.SizeBDiagCursor)
            elif 0 <= xPos <= self.Margins <= yPos <= hm:
                # 左边
                self.Direction = Left
                self.setCursor(Qt.SizeHorCursor)
            elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
                # 右边
                self.Direction = Right
                self.setCursor(Qt.SizeHorCursor)
            elif wm >= xPos >= self.Margins >= yPos >= 0:
                # 上面
                self.Direction = Top
                self.setCursor(Qt.SizeVerCursor)
            elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
                # 下面
                self.Direction = Bottom
                self.setCursor(Qt.SizeVerCursor)
        except Exception as e:
            print("鼠标移动事件异常：%s" % e)

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        try:
            if self.Direction is None:
                return
            mpos = pos - self._mpos
            xPos, yPos = mpos.x(), mpos.y()
            geometry = self.geometry()
            x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
            if self.Direction == LeftTop:  # 左上角
                if w - xPos > self.minimumWidth():
                    x += xPos
                    w -= xPos
                if h - yPos > self.minimumHeight():
                    y += yPos
                    h -= yPos
            elif self.Direction == RightBottom:  # 右下角
                if w + xPos > self.minimumWidth():
                    w += xPos
                    self._mpos = pos
                if h + yPos > self.minimumHeight():
                    h += yPos
                    self._mpos = pos
            elif self.Direction == RightTop:  # 右上角
                if h - yPos > self.minimumHeight():
                    y += yPos
                    h -= yPos
                if w + xPos > self.minimumWidth():
                    w += xPos
                    self._mpos.setX(pos.x())
            elif self.Direction == LeftBottom:  # 左下角
                if w - xPos > self.minimumWidth():
                    x += xPos
                    w -= xPos
                if h + yPos > self.minimumHeight():
                    h += yPos
                    self._mpos.setY(pos.y())
            elif self.Direction == Left:  # 左边
                if w - xPos > self.minimumWidth():
                    x += xPos
                    w -= xPos
                else:
                    return
            elif self.Direction == Right:  # 右边
                if w + xPos > self.minimumWidth():
                    w += xPos
                    self._mpos = pos
                else:
                    return
            elif self.Direction == Top:  # 上面
                if h - yPos > self.minimumHeight():
                    y += yPos
                    h -= yPos
                else:
                    return
            elif self.Direction == Bottom:  # 下面
                if h + yPos > self.minimumHeight():
                    h += yPos
                    self._mpos = pos
                else:
                    return
            self.setGeometry(x, y, w, h)
        except Exception as e:
            print("调整窗口大小异常：%s" % e)

    @staticmethod
    def typeface_function():
        """ 设置字体功能关联 """
        global son_window
        son_window.shuncom_set_font_color()


    def about(self):
        """关于"""
        global son_window
        son_window.version_show()

    def shuncom_close(self):
        """ 退出程序 """
        global son_window
        reply = QMessageBox.question(
            self, '退出程序', "您是否要退出程序?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            son_window.Save_Window_Data()
            self.close()
        else:
            return

class shuncom_MainWindow(QWidget):
    """ 在窗口框架中添加 UI控件 """

    def __init__(self, *args, **kwargs):
        super(shuncom_MainWindow, self).__init__(*args, **kwargs)
        global son_window
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        son_window = ShuncomWidget()

        layout.addWidget(son_window)

if __name__ == '__main__':
    pass
