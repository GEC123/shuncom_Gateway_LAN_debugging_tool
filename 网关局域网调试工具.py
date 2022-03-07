#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员:周标华
# time: 2022-01-11 14:04
# 文件名称: 网关局域网调试工具.PY
# 开发工具: PyCharm
# Version: 1.0.0
"""
声明：程序入口
"""

import sys
from PyQt5.QtCore import QSize, QTranslator

from PyQt5.QtWidgets import QApplication #,QVBoxLayout,QWidget
from PyQt5.QtGui import QIcon

#+++++++++++++++++++++++++++功能模块+++++++++++++++++++++++++++++++++++++++++++=
from shuncom_module.shuncom_params_init import *
from shuncom_ui.shuncom_main_3 import shuncom_FramelessWindow,shuncom_MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/png/shuncom_ico/png_ico2/检测.ico'))
    app.setStyleSheet(StyleSheet)
    mainWnd = shuncom_FramelessWindow()
    mainWnd.setWindowTitle('网关局域网调试工具')
    #mainWnd.setWindowIcon(QIcon(':/png/shuncom_ico/png_ico2/检测.ico'))
    mainWnd.resize(QSize(1282, 812))
    mainWnd.setWidget(shuncom_MainWindow(mainWnd))  # 把自己的窗口添加进来
    # mainWnd.setWindowOpacity(0.95)
    mainWnd.show()
    QApplication.processEvents()
    sys.exit(app.exec_())

# 编译打包
# pyinstaller -F -w -i 文件名.ico 文件名.py
# pyinstaller -F -w -i tool.ico 网关局域网调试工具.py
# pyinstaller -F -w  网关局域网调试工具.py
# pyinstaller --distpath www/ -w -i 检测.ico --clean 网关局域网调试工具.py

# ico图标 内置编译
# pyrcc5 shuncom_ui\shuncom_qrc.qrc -o shuncom_qrc_rc.py

# PyQt5中实现界面语言国际化 pylupdate5 xx.py  -ts   xxxx  -ts
# pylupdate5 .\shuncom_ui\tool_main.py -ts .\shuncom_ui\shuncom_en.ts
# pylupdate5 .\shuncom_ui\tool_main.py -ts .\shuncom_ui\shuncom_zh_cn.ts