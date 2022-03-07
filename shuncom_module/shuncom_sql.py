import sqlite3
import traceback
import os
import time
import win32api

tools_route = '.\shuncom_tools\sqlitestudio_3.3.3\SQLiteStudio\SQLiteStudio.exe'

def sql_open():
    '''打开方案数据库'''
    try:
        re = win32api.ShellExecute(None, 'runas', '%s' % tools_route, '.\Config\ConfigIni_plan.db', None, 1)
        if re > 32:
            return True
        else:
            return False
    except Exception as e:
        print(traceback.print_exc())


def sql_table_creat(planname):
    '''创建新的表格'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        plansql = sql.cursor()  #数据库实例化一个对象
        plansql.execute('''CREATE TABLE IF NOT EXISTS '%s'(
                    设备类别 TEXT,
                    MAC地址 TEXT PRIMARY KEY NOT NULL,
                    固件版本号 TEXT,
                    硬件型号 TEXT,
                    连接方式 TEXT,
                    设备IP地址 TEXT,
                    HTTP端口 TEXT,
                    子网掩码 TEXT,
                    'SZIOT服务器IP地址:端口' TEXT,
                    'SZTT服务器IP地址:端口' TEXT,
                    'MQTT服务器IP地址:端口' TEXT,
                    Zigbee频点 TEXT, 
                    Zigbee频点ID TEXT);''' % planname)
        sql.commit()#数据库提交
        sql.close()#断开连接
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())

def sql_delete_table(planname):
    '''删除指定表格'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        plansql = sql.cursor()  # 数据库实例化一个对象
        plansql.execute('''DROP TABLE '%s' ''' % planname)
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        return True
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())
        return False

def sql_write(planname,WindowData):
    '''写入指令数据到数据库指定表格'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        plansql = sql.cursor()  # 数据库实例化一个对象
        plansql.execute('''INSERT INTO '%s'(
                                        设备类别, MAC地址, 固件版本号, 硬件型号, 连接方式, 设备IP地址, HTTP端口, 子网掩码, 'SZIOT服务器IP地址:端口', 'SZTT服务器IP地址:端口', 'MQTT服务器IP地址:端口', Zigbee频点, Zigbee频点ID
                                        ) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (planname, WindowData[0],
                                        WindowData[1], WindowData[2], WindowData[3], WindowData[4], WindowData[5], WindowData[6], WindowData[7],
                                        WindowData[8], WindowData[9], WindowData[10], WindowData[11], WindowData[12]))

        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())

def dict_factory(cursor, row):
    '''指定放回的数据形式'''
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


def sql_read(planname, MAC, mode = 1):
    '''读取数据库对应表格中的指令数据'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        sql.row_factory = dict_factory #指定工厂方法为自定义方法
        plansql = sql.cursor()  # 数据库实例化一个对象
        if mode == 1:#读取单个指令数据
            SqlData = plansql.execute('''SELECT * FROM '%s' WHERE MAC地址 = '%s' ''' % (planname, MAC))
            SqlData = SqlData.fetchall()
            if len(SqlData) == 0:
                return None
            SqlData = SqlData[0]
        if mode == 2:#获取全部指令数据
            SqlData = plansql.execute('''SELECT * FROM '%s' ''' % (planname))
            SqlData = SqlData.fetchall()
            if len(SqlData) == 0:
                return None
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        return SqlData
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())
        return None

def sql_updata(planname, MAC, attribute, VALUE):
    '''更新数据库中的数据'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        sql.row_factory = dict_factory  # 指定工厂方法为自定义方法
        plansql = sql.cursor()  # 数据库实例化一个对象
        plansql.execute('''UPDATE '%s' SET '%s' = '%s' WHERE MAC地址 = '%s' ''' % (planname, attribute, VALUE, MAC))
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())

def sql_delete_data(planname, MAC, mode = 1):
    '''删除数据库中的指令数据,mode = 1删除指定的某条指令数据,mode = 2删除所有的指令数据'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')#连接数据库，没有就创建
        sql.row_factory = dict_factory  # 指定工厂方法为自定义方法
        plansql = sql.cursor()  # 数据库实例化一个对象
        if mode == 1:
            plansql.execute('''DELETE FROM '%s' WHERE MAC地址 = '%s' ''' % (planname,MAC))
        if mode == 2:
            plansql.execute('''DELETE FROM '%s' ''' % (planname))
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())

def sql_show_table():
    '''获取数据库中的所有表名'''
    try:
        sql = sqlite3.connect('./Config/ConfigIni_plan.db')  # 连接数据库，没有就创建
        sql.row_factory = dict_factory  # 指定工厂方法为自定义方法
        plansql = sql.cursor()  # 数据库实例化一个对象
        plansql.execute('''select name from sqlite_master where type='table' order by name''')
        tablelist = plansql.fetchall()
        if len(tablelist) == 1:
            tablename = [tablelist[0]['name']]
        else:
            tablename = []
            for i in tablelist:
                tablename.append(i['name'])
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        return tablename
    except Exception as e:
        sql.commit()  # 数据库提交
        sql.close()  # 断开连接
        print(traceback.print_exc())


