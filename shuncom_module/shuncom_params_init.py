#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 开发人员:王灋權
"""
默认参数配置：
创建日志文件路径
创建日志级别
创建配置文件
"""

import configparser
import os

content = r'''
[LOG]
explain__config_level = #日志级别:DEBUG,INFO,WARNING,ERROR,CRITICAL
config_level = DEBUG
explain__config_set_log_level = #日志文件级别级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
config_set_log_level = DEBUG
explain__config_file_log = #文件日志开关, True 表示开启, False 值关闭
config_file_log = True
explain__config_log_name = #log文件名称创建
config_log_name = 
config_log_name_list = []


[FONT_COLOR]
; 中英文切换标志
config_en_zn_on_off = 1
;设置字体大小和字体颜色
config_font_size = 10.0
;设置字体颜色
config_font_color = 
;设置背景图片
config_background = shuncom_ico/bj2.png
;设置窗口模版样式
config_style = 


[CONFIG_SHUNCOM]
; 配置页面保存参数
tableWidget_column = 
search_set_data =

'''

if not os.path.exists('.\Config'):
    os.mkdir('.\Config')

if not os.path.exists('.\Config/Config.ini'):
    with open('.\Config/Config.ini', 'w', encoding='utf-8-sig') as f:
        f.write(content)

config_init = configparser.ConfigParser()
config_init.read('.\Config/Config.ini', encoding='utf-8-sig')

if not os.path.exists('.\Results'):
    os.mkdir('.\Results')
result_path = '.\Results/'

if not os.path.exists('.\Logs'):
    os.mkdir('.\Logs')
log_path = '.\Logs\log/'

if not os.path.exists('.\Logs\LogError'):
    os.mkdir('.\Logs\LogError')
shuncomError_path = '.\Logs\LogError/'

if not os.path.exists('.\Results\Export_data'):
    os.makedirs('.\Results\Export_data')
Export_path = '.\Results\Export_data'

if not os.path.exists('.\HelpBook'):
    os.makedirs('.\HelpBook')

#################################################################
# LOG  #日志
config_log_level = config_init.get('LOG', 'config_level')
config_set_log_level = config_init.get('LOG', 'config_set_log_level')
config_file_log = config_init.get('LOG', 'config_file_log')
config_log_name = config_init.get('LOG', 'config_log_name')
config_log_name_list = config_init.get('LOG', 'config_log_name_list')

# FONT_COLOR  #UI
config_font_size = config_init.get('FONT_COLOR', 'config_font_size')
config_font_color = config_init.get('FONT_COLOR', 'config_font_color')
config_background = config_init.get('FONT_COLOR', 'config_background')
config_style = config_init.get('FONT_COLOR', 'config_style')
# UI_SET_SWITCH  #中文英文
config_en_zn_on_off = config_init.get('FONT_COLOR', 'config_en_zn_on_off')
# CONFIG_SHUNCOM  配置界面数据
config_tablewidget_column = config_init.get('CONFIG_SHUNCOM', 'tableWidget_column')
config_search_set_data = config_init.get('CONFIG_SHUNCOM', 'search_set_data')
# =========================== 其他 =================================================


# 样式
StyleSheet = """
/*标题栏*/
TitleBar{
    background-color: rgb(21, 133, 212);
}
/*按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose,#about_pushbutton,#typeface_pushbutton {
    border:none;
    background-color:#1585D4;
    border-bottom:1px solid #1585D4;
    border-radius:1px;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/*悬停状态*/
#buttonClose:hover{
    background-color: red;
    color:  rgb(21, 133, 212);
}
#buttonMinimum:hover,#buttonMaximum:hover,#about_pushbutton:hover,#typeface_pushbutton:hover{
    background-color: #b8b8b8;
    color:  rgb(21, 133, 212);
}


/*按下状态*/
#buttonMinimum:pressed,#buttonMaximum:pressed,#buttonClose:pressed,
#about_pushbutton:pressed,#typeface_pushbutton:pressed{
	background-color: rgb(170 , 255 , 255);
	color: white;
}


/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(170 , 255 , 255);
}
#buttonClose:pressed {
    color: white;
    background-color: Firebrick;
}

"""

QPushButtoStyle1 = """
/*按钮普通态*/
QPushButton
{
    /*字体为微软雅黑*/
    font-family:Microsoft Yahei;
    /*字体大小为20点*/
    font-size:10pt;
    /*字体颜色*/ 
	color: rgb(50, 50, 51);
 	/*背景颜色*/  
	background-color: rgb(255, 255, 255);
    /*边框圆角半径为8像素*/ 
    border-radius:2px;
    icon : url(:/png/shuncom_ico/png_ico/右箭头.png);
	width:65px;
}

/*按钮停留态*/
QPushButton:hover
{
	icon : url(:/png/shuncom_ico/png_ico/右箭头-红.png);
}

/*按钮按下态*/
QPushButton:pressed
{

    icon : url(:/png/shuncom_ico/png_ico/右箭头-红.png);
    /*左内边距为3像素，让按下时字向右移动3像素*/  
    padding-left:3px;
    /*上内边距为3像素，让按下时字向下移动3像素*/  
    padding-top:3px;
}
"""

QPushButtoStyle2 = """
/*按钮普通态*/
QPushButton
{
    /*字体为微软雅黑*/
    font-family:Microsoft Yahei;
    /*字体大小为20点*/
    font-size:10pt;
    /*字体颜色*/ 
	color: rgb(50, 50, 51);
 	/*背景颜色*/  
	background-color: rgb(255, 255, 255);
    /*边框圆角半径为8像素*/ 
    border-radius:2px;
    icon : url(:/png/shuncom_ico/png_ico/左箭头.png);
	width:65px;
}

/*按钮停留态*/
QPushButton:hover
{
	icon : url(:/png/shuncom_ico/png_ico/左箭头-红.png);
}

/*按钮按下态*/
QPushButton:pressed
{

    icon : url(:/png/shuncom_ico/png_ico/左箭头-红.png);
    /*左内边距为3像素，让按下时字向右移动3像素*/  
    padding-left:3px;
    /*上内边距为3像素，让按下时字向下移动3像素*/  
    padding-top:3px;
}
"""

comboxBarStyle = """
QComboBox{
    /*字体为微软雅黑*/
    font-family:Microsoft Yahei;
    /*字体大小为20点*/
    font-size:9pt;
    /*字体颜色*/ 
	color: rgb(50, 50, 51);
	border : none;
}
QComboBox::down-arrow{
	image: url(:/png/shuncom_ico/png_ico/下箭头.png);
	hight : 16px;
	width : 16px;
	
}
QComboBox::down-arrow:on{
	image: url(:/png/shuncom_ico/png_ico/上箭头.png);
	hight : 16px;
	width : 16px;
}
/* 设置为可编辑editable时，点击下拉框的样式 */
QComboBox::drop-down:editable:on {
    image: url(:/png/shuncom_ico/png_ico/上箭头.png);
	hight : 16px;
	width : 16px;
}
QComboBox::drop-down{
	border-style: none;
}
"""

comboxBarStyle_offline = """
QComboBox{
    /*字体为微软雅黑*/
    font-family:Microsoft Yahei;
    /*字体大小为20点*/
    font-size:9pt;
    /*字体颜色*/ 
	color: rgb(50, 50, 51);
	background-color:rgb(200, 201, 204);
	border : none;
}
QComboBox::down-arrow{
	image: url(:/png/shuncom_ico/png_ico/下箭头.png);
	hight : 16px;
	width : 16px;

}
QComboBox::down-arrow:on{
	image: url(:/png/shuncom_ico/png_ico/上箭头.png);
	hight : 16px;
	width : 16px;
}
/* 设置为可编辑editable时，点击下拉框的样式 */
QComboBox::drop-down:editable:on {
    image: url(:/png/shuncom_ico/png_ico/上箭头.png);
	hight : 16px;
	width : 16px;
}
QComboBox::drop-down{
	border-style: none;
}
"""

'''垂直滚动条样式'''
verticalScrollBarStyle = """
/*普通状态*/
QScrollBar
{
    /*宽度设置*/
    width: 10px;
}
"""

'''水平滚动条样式'''
horizontalScrollBarStyle = """
/*普通状态*/
QScrollBar
{
    /*高度设置*/
    height:10px;
}
"""
