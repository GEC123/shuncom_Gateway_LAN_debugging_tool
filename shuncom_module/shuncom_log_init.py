#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 开发人员:王灋權
"""
日志文件创建、日志文件路径、日志文件级别
"""


# ----------------------------------------------------------
from shuncom_module.shuncom_params_init import config_log_level, config_file_log, \
    log_path,config_set_log_level,config_init,shuncomError_path
# ----------------------------------------------------------

import os
import time
import logging
import logging.handlers
from PyQt5.QtCore import QObject
from PyQt5 import QtCore


class Handler(QObject, logging.Handler):
    """ Handler """
    if not os.path.exists('Logs\log'):
        os.mkdir('Logs\log')
    if not os.path.exists('Logs\LogError'):
        os.mkdir('Logs\LogError')
    new_record = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        super(logging.Handler).__init__()

    def emit(self, record):
        """ emit """
        msg = self.format(record)
        self.new_record.emit(msg)


handler = Handler()




class Shuncom_Log():
    """ 顺舟工具 日志 """

    def __init__(self):
        super(Shuncom_Log, self).__init__()
        # formatter = logging.Formatter('%(asctime)s %(name)s- %(levelname)s - %(message)s')  #没有代码行
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")


    @staticmethod
    def log_name_time():
        """创建log文件的名称"""
        log_name_time_time = time.strftime('%Y%m%d', time.localtime(time.time()))  # 创建已天为单位的文件
        # log_name_time_time = time.strftime('%Y%m%d_%H%m%S', time.localtime(time.time())) # 创建以秒为单位的文件
        config_init.set("LOG", "config_log_name", log_name_time_time)
        config_init.write(open("Config/Config.ini", "w", encoding='utf-8-sig'))
        return log_name_time_time


    def shuncom_log(self):
        """ log 级别"""
        # 日志文件级别级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
        logging.getLogger().addHandler(handler)
        if config_set_log_level == 'CRITICAL':
            log_dj = logging.CRITICAL
        elif config_set_log_level == 'ERROR':
            log_dj = logging.ERROR
        elif config_set_log_level == 'WARNING':
            log_dj = logging.WARNING
        elif config_set_log_level == 'INFO':
            log_dj = logging.INFO
        else:
            log_dj = logging.DEBUG

        logging.getLogger().setLevel(log_dj)  # 读取config配置中 日志等级
        logging.getLogger("paramiko.transport").setLevel(logging.WARNING)  # 屏蔽paramiko程序的WARNING以下日志
        logging.StreamHandler().setFormatter(self.formatter)

        rq = self.log_name_time()
        log_name = '%slog_%s.log' % (log_path, rq)  # 固件文件名称
        if config_file_log == 'True':
            fh = logging.FileHandler(log_name)  # 写入日志文件
            fh.setLevel(logging.DEBUG)  # 日志文件级别级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
            fh.setFormatter(self.formatter)
            logging.getLogger().addHandler(fh)
        return logging


    def shuncom_Error_methods(self):
        """ shuncom_Error """
        # 日志文件级别级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
        logging.getLogger().addHandler(handler)
        if config_set_log_level == 'CRITICAL':
            log_dj = logging.CRITICAL
        elif config_set_log_level == 'ERROR':
            log_dj = logging.ERROR
        elif config_set_log_level == 'WARNING':
            log_dj = logging.WARNING
        elif config_set_log_level == 'INFO':
            log_dj = logging.INFO
        else:
            log_dj = logging.DEBUG

        logging.getLogger().setLevel(log_dj)  # 读取config配置中 日志等级
        logging.getLogger("paramiko.transport").setLevel(logging.WARNING)  # 屏蔽paramiko程序的WARNING以下日志
        logging.StreamHandler().setFormatter(self.formatter)

        rq = self.log_name_time()
        log_name = '%sError_%s.log' % (shuncomError_path, rq)  # 固件文件名称
        fh = logging.FileHandler(log_name)  # 写入日志文件
        fh.setLevel(logging.ERROR)  # 日志文件级别级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
        fh.setFormatter(self.formatter)
        logging.getLogger().addHandler(fh)
        return logging


level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

level = level_map[config_log_level.lower()]
sz_log_record = Shuncom_Log().shuncom_log()
sz_log_Error = Shuncom_Log().shuncom_Error_methods()
