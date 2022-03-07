#######################################系统模块#####################################
import re
import os
import time
import json
import socket
import _thread
import threading
import traceback
import subprocess
import shutil
import base64
import psutil
import random
from multiprocessing import Process
from Crypto.Cipher import AES
from http.server import HTTPServer, CGIHTTPRequestHandler
######################################自定义模块#####################################
from shuncom_ui.shuncom_main_1 import MainWindow_main_1



def thread_it(func, *args):
    """将函数打包进线程"""
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

def now_time_s():
    """运行时间："""
    now = time.strftime('%Y-%m-%d %X', time.localtime()) +': '  # 获取当前的时间
    return now

def hex2dec(string_num):
    """16进制转10进制 """
    return str(int(string_num.upper(), 16))

def D_to_H(data):
    '''十进制转十六进制'''
    if data == None:
        return
    data_radio = int(data)  # 十进制整数转十六进制整数再转字符串
    if data_radio <= 16:
        data_radio = '0' + str(hex(data_radio)).replace('0x', '')
    else:
        data_radio = str(hex(data_radio)).replace('0x', '')
    data_radio = data_radio.upper()
    if len(data_radio) % 2 != 0:
        data_radio = '0' + data_radio
    return data_radio

def udp_same_scanning(local_netcard):
    """扫描同网段网关数据"""
    try:
        global udp_recv_dict  # 存放所有消息的字典
        udp_recv_dict = {}
        # 获取网关基本信息
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.bind(('', 9999))  # 电脑ip和端口

        _thread.start_new_thread(recv_message, (1, udp_client))
        local_ip = get_local_ip()
        find_ip(local_netcard, '1', '255', udp_client, random_sysinfo(), local_ip)
        time.sleep(1)
        udp_client.close()

        if len(udp_recv_dict) != 0:
            udp_socker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            localaddr = ('', 9999)
            udp_socker.bind(localaddr)
            '''对已经获取到的所有IP地址进行更多信息获取'''
            Acquired_IP_list = list(udp_recv_dict.keys())
            _thread.start_new_thread(recv_message, (len(Acquired_IP_list), udp_socker))
            for mac in Acquired_IP_list:  # 获取子网掩码和http端口
                ip = udp_recv_dict[mac]['ipaddr']
                proto = udp_recv_dict[mac]['proto']
                udp_socker.sendto(aes_encrypt(random_network(mac, proto)), (ip, 8887))
            for mac in Acquired_IP_list:  # 获取服务器指向数据
                ip = udp_recv_dict[mac]['ipaddr']
                send_data = aes_encrypt(random_cloud_config(mac))
                udp_socker.sendto(send_data, (ip, 8887))
            for mac in Acquired_IP_list:  # 获取bdinfo数据
                ip = udp_recv_dict[mac]['ipaddr']
                udp_socker.sendto(aes_encrypt(random_bdinfo(mac)), (ip, 8887))
            time.sleep(1)
            udp_socker.close()

            udp_socker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            localaddr = ('', 9999)
            udp_socker.bind(localaddr)
            _thread.start_new_thread(recv_message, (len(Acquired_IP_list), udp_socker))
            for mac in Acquired_IP_list:  # 获取频点和频点ID
                ip = udp_recv_dict[mac]['ipaddr']
                bdinfo_mode = udp_recv_dict[mac]['bdinfo']
                udp_socker.sendto(aes_encrypt(random_module_config(mac, bdinfo_mode)), (ip, 8887))
            time.sleep(1)
            udp_socker.close()

            device_tpye_divide()  # 进行设备类型区分
        if udp_recv_dict:
            return udp_recv_dict
        else:
            return None
    except Exception as e:
        print(traceback.print_exc())


def recv_message(time_t, udp_socket):
    global udp_recv_dict    # 存放所有接收数据的字典， 根据IP进行查找

    time_tt = (3 * int(time_t))
    udp_socket.settimeout(time_tt)  # 获取套接字默认超时时间10秒
    try:
        while True:
            try:
                device_list, addr = udp_socket.recvfrom(8888)
            except Exception as e:
                if '10054' in str(e):
                    continue
            if device_list == None:
                continue
            # print(device_list)
            device_list = aes_decrypt(device_list)
            device_list['addr'] = addr
            # print(device_list)
            # 判断IP是否已存在,不存在就创建
            if device_list['deviceId'] not in udp_recv_dict:
                udp_recv_dict[device_list['deviceId']] = {}
            #进行模块判断
            if 'module' in device_list:
                if device_list['module'] == 'sysinfo':
                    udp_recv_dict[device_list['deviceId']]['ipaddr'] = device_list['addr'][0]
                    if 'version' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['version'] = device_list['properties']['version'] # 获取固件版本号
                    else:
                        udp_recv_dict[device_list['deviceId']]['version'] = '无'

                    if 'HW_model' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['HW_model'] = device_list['properties']['HW_model'] # 获取硬件型号
                    else:
                        udp_recv_dict[device_list['deviceId']]['HW_model'] = '无'

                    if 'proto' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['proto'] = device_list['properties']['proto']  # 获取连接方式
                    else:
                        udp_recv_dict[device_list['deviceId']]['proto'] = '无'

                    if 'deviceId' in device_list:
                        udp_recv_dict[device_list['deviceId']]['deviceId'] = device_list['deviceId']  # 设备ID
                    else:
                        udp_recv_dict[device_list['deviceId']]['deviceId'] = '无'

                    if "storage_size" in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['storage_size'] = device_list['properties']['storage_size']  # 设备剩余内存
                    else:
                        udp_recv_dict[device_list['deviceId']]['storage_size'] = '无'

                elif device_list['module'] == 'bdinfo':
                    if 'MODULE' in device_list["properties"]:
                        for i in range(len(device_list["properties"]['MODULE'])):   # 找到模块是zigbee5_0的那个字典
                            if "zigbee5_0" == device_list["properties"]['MODULE'][i]['model']:
                                udp_recv_dict[device_list['deviceId']]['bdinfo'] = device_list['properties']['MODULE'][i]['name']   # 获取频点类型

            if 'function' in device_list:
                if device_list['function'] == 'wan_read':
                    if 'http_port' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['http_port'] = device_list['properties']['http_port']  # 获取HTTP端口
                    else:
                        udp_recv_dict[device_list['deviceId']]['http_port'] = '无'

                    if 'netmask' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['netmask'] = device_list['properties']['netmask']  # 获取子网掩码
                    else:
                        udp_recv_dict[device_list['deviceId']]['netmask'] = '无'

                    if 'ipaddr' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['ipaddr'] = device_list['properties']['ipaddr']  # 获取设备IP
                    else:
                        udp_recv_dict[device_list['deviceId']]['ipaddr'] = '无'

                    if 'mode' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['mode'] = device_list['properties']['mode']
                    else:
                        udp_recv_dict[device_list['deviceId']]['mode'] = '无'

                    if udp_recv_dict[device_list['deviceId']]['proto'] == 'static':
                        if 'gateway' in device_list['properties']:
                            udp_recv_dict[device_list['deviceId']]['gateway'] = device_list['properties']['gateway']  # 获取设备网关
                        else:
                            udp_recv_dict[device_list['deviceId']]['gateway'] = '无'

                        if 'dns_flag' in device_list['properties']:
                            udp_recv_dict[device_list['deviceId']]['dns_flag'] = device_list['properties']['dns_flag']  # DNS启用标志
                        else:
                            udp_recv_dict[device_list['deviceId']]['dns_flag'] = '1'

                        if 'dns1' in device_list['properties']:
                            udp_recv_dict[device_list['deviceId']]['dns1'] = device_list['properties']['dns1']  # 首选DNS
                        else:
                            udp_recv_dict[device_list['deviceId']]['dns1'] = '114.114.114.114'

                        if 'dns2' in device_list['properties']:
                            udp_recv_dict[device_list['deviceId']]['dns2'] = device_list['properties']['dns2']  # 备选DNS
                        else:
                            udp_recv_dict[device_list['deviceId']]['dns2'] = '8.8.8.8'


                elif device_list['function'] == 'cloud_config_read':
                    if 'sziot' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['sziot'] = device_list['properties']['sziot']  # 获取SZIOT服务器指向
                    else:
                        udp_recv_dict[device_list['deviceId']]['sziot'] = '无'

                    if 'sztt_cloud' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['sztt_cloud'] = device_list['properties']['sztt_cloud']  # 获取SZTT服务器指向
                    else:
                        udp_recv_dict[device_list['deviceId']]['sztt_cloud'] = '无'

                    if 'mqtt_server' in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['mqtt_server'] = device_list['properties']['mqtt_server']  # 获取MQTT服务器指向
                    else:
                        udp_recv_dict[device_list['deviceId']]['mqtt_server'] = '无'

                elif device_list['function'] == 'module_config_read':
                    function = '%s@MODULE' % udp_recv_dict[device_list['deviceId']]['bdinfo']
                    # print(function)
                    if function in device_list['properties']:
                        udp_recv_dict[device_list['deviceId']]['channel'] = device_list['properties'][function]['channel']  # 获取频点
                        udp_recv_dict[device_list['deviceId']]['pan_id'] = device_list['properties'][function]['pan_id']  # 获取频点ID
                    else:
                        udp_recv_dict[device_list['deviceId']]['channel'] = '无'
                        udp_recv_dict[device_list['deviceId']]['pan_id'] = '无'
            device_list = None
        # print(udp_recv_dict)
    except Exception as e:
        # 5. 关闭套接字
        udp_socket.close()
        # print(traceback.print_exc())


def device_tpye_divide():
    global udp_recv_dict
    '''设备类型划分'''
    try:
        key_list = list(udp_recv_dict.keys())
        for key in key_list:
            if udp_recv_dict[key]['HW_model'] == 'SZ11-GW-7':   # 聚盒4
                udp_recv_dict[key]['device_type'] = '聚盒四代'
            if udp_recv_dict[key]['HW_model'] == 'SZ11-GW-8':   # 聚盒5
                udp_recv_dict[key]['device_type'] = '聚盒五代'
            if udp_recv_dict[key]['HW_model'] == 'SZ11-CBOX-4':     # 云盒4
                udp_recv_dict[key]['device_type'] = '云盒四代'
            if udp_recv_dict[key]['HW_model'] == 'SZ10-GW-4_V4':    # 星盒
                udp_recv_dict[key]['device_type'] = '星盒'
    except Exception as e:
        print(traceback.print_exc())

    ############################################协议指令函数#############################################
def random_sysinfo():
    '''获取基础配置信息指令'''
    try:
        t = time.time()
        send_data = '''{
        "timestamp": %d, 
        "messageId": %d, 
        "passwd": "shuncom",
        "module": "sysinfo",
        "properties": ["macaddr", "HW_model", "version", "proto", "storage_size"], 
        "topic": "/+/+/properties_read", 
        "type": "sub"
        }''' % (int(round(t * 1000)), int(t))
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_network(deviceId, proto):
    '''获取http端口指令'''
    try:
        t = time.time()
        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = "shuncom"
        send_data["function"] = "wan_read"
        if proto == 'static':
            send_data["properties"] = ["ipaddr", "http_port", "netmask", "mode", "gateway", "dns_flag", "dns1", "dns2"]
        else:
            send_data["properties"] = ["ipaddr", "http_port", "netmask", "mode"]
        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        # print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_bdinfo(deviceId):
    '''获取bdinfo指令'''
    try:
        t = time.time()
        send_data = '''{
            "timestamp": %d,
            "messageId": %d,
            "deviceId": "%s",
            "passwd": "shuncom",
            "module":"bdinfo",
            "properties":["MODULE"],
            "topic": "/+/+/properties_read",
            "type": "sub"
        }''' % (int(round(t * 1000)), int(t), deviceId)
        return send_data
    except Exception as e:
        print(traceback.print_exc())


def random_cloud_config(deviceId):
    '''获取服务器指向信息指令'''
    try:
        t = time.time()
        send_data = '''{
            "timestamp": %d,
            "messageId": %d,
            "deviceId": "%s",
            "passwd": "shuncom",
            "function":"cloud_config_read",
            "properties": ["sziot", "sztt_cloud", "mqtt_server"],
            "topic": "/+/+/function_invoke",
            "type": "sub"
        }''' % (int(round(t * 1000)), int(t), deviceId)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_module_config(deviceId, bdinfotype):
    '''获取Zigbee频点指令'''
    try:
        t = time.time()
        send_data = '''{
            "timestamp": %d,
            "messageId": %d,
            "deviceId": "%s",
            "passwd": "shuncom",
            "function":"module_config_read",
            "properties": ["%s@MODULE"],
            "topic": "/+/+/function_invoke",
            "type": "sub"
        }''' % (int(round(t * 1000)), int(t), deviceId, bdinfotype)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_change_zigbee(deviceId, passwd, name, channel, pan_id):
    '''修改Zigbee频点指令'''
    try:
        t = time.time()
        send_data = '''{
                "timestamp": %d,
                "messageId": %d,
                "deviceId": "%s",
                "passwd": "%s",
                "function":"module_config_write",
                "properties": {"%s@MODULE": {"channel": %d, "pan_id": %d}},
                "topic": "/+/+/function_invoke",
                "type": "sub"
            }''' % (int(round(t * 1000)), int(t), deviceId, passwd, name, channel, pan_id)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_change_erver(deviceId, passwd, server_order_data):
    '''修改服务器指向'''
    try:
        t = time.time()
        properties = {'sziot': [], 'sztt_cloud': [], 'mqtt_server': []}
        sziot_key_list = list(server_order_data['sziot'].keys())
        sztt_key_list = list(server_order_data['sztt'].keys())
        mqtt_key_list = list(server_order_data['mqtt'].keys())
        for count in range(len(sziot_key_list)):
            properties['sziot'].append({sziot_key_list[count]: server_order_data['sziot'][sziot_key_list[count]]})
        for count in range(len(sztt_key_list)):
            properties['sztt_cloud'].append({sztt_key_list[count]: server_order_data['sztt'][sztt_key_list[count]]})
        for count in range(len(mqtt_key_list)):
            mqtt_broker = server_order_data['mqtt'][mqtt_key_list[count]]['mqtt_broker']
            host = mqtt_key_list[count].split(':')[0]
            port = mqtt_key_list[count].split(':')[1]
            properties['mqtt_server'].append({mqtt_broker: {}})
            print(properties)
            properties['mqtt_server'][count][mqtt_broker]['username'] = server_order_data['mqtt'][mqtt_key_list[count]]['username']
            properties['mqtt_server'][count][mqtt_broker]['passwd'] = server_order_data['mqtt'][mqtt_key_list[count]]['passwd']
            properties['mqtt_server'][count][mqtt_broker]['port'] = port
            properties['mqtt_server'][count][mqtt_broker]['pubqos'] = server_order_data['mqtt'][mqtt_key_list[count]]['pubqos']
            properties['mqtt_server'][count][mqtt_broker]['host'] = host

        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = passwd
        send_data["function"] = "cloud_config_write"
        send_data["properties"] = properties
        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_initialization(deviceId, passwd):
    '''设备初始化指令'''
    try:
        t = time.time()
        send_data = '''{
                            "timestamp": %d,
                            "messageId": %d,
                            "deviceId": "%s",
                            "passwd": "%s",
                            "function":"factory_data_reset",
                            "topic": "/+/+/function_invoke",
                            "type": "sub"
                        }''' % (int(round(t * 1000)), int(t), deviceId, passwd)
        return send_data
    except Exception as e:
        print(traceback.print_exc())


def random_reboot(deviceId, passwd):
    '''立即重启指令'''
    try:
        t = time.time()
        send_data = '''{
                    "timestamp": %d,
                    "messageId": %d,
                    "deviceId": "%s",
                    "passwd": "%s",
                    "function":"reboot",
                    "topic": "/+/+/function_invoke",
                    "type": "sub"
                }''' % (int(round(t * 1000)), int(t), deviceId, passwd)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_timing_reboot(deviceId, passwd, reboot_data):
    '''定时重启指令'''
    try:
        t = time.time()
        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = passwd
        send_data["function"] = "auto_reboot"
        if reboot_data['enable'] == '1':
            send_data["properties"] = {'days': reboot_data['days'], 'enable': reboot_data['enable'], 'hour': reboot_data['hour'], 'min': reboot_data['min']}
        else:
            send_data["properties"] = {'enable': reboot_data['enable']}

        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_cheak_timing(deviceId, passwd, timing_data):
    '''校时指令'''
    try:
        t = time.time()
        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = passwd
        send_data["function"] = "sync_time"
        if timing_data['enabled'] == '1':
            send_data["properties"] = {
                'enabled': timing_data['enabled'],
                'server': timing_data['server'],
                'port': timing_data['port'],
                "sync_interval": timing_data['sync_interval']
            }
        else:
            send_data["properties"] = {'enabled': timing_data['enabled']}

        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_firmware_updata(deviceId, passwd, md5, url):
    '''固件升级指令'''
    try:
        t = time.time()
        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = passwd
        send_data["function"] = "firmware_update"
        send_data["properties"] = {"md5": md5, 'url': url}
        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

def random_change_network_info(deviceId, passwd, mode, network_data):
    '''修改网络配置'''
    try:
        t = time.time()
        send_data = {}
        send_data["timestamp"] = int(round(t * 1000))
        send_data["messageId"] = int(t)
        send_data["deviceId"] = deviceId
        send_data["passwd"] = passwd
        send_data["function"] = "wan_write"
        if network_data["proto"] == 'static':
            send_data["properties"] = {
                "mode": mode,
                "proto": network_data["proto"],
                "ipaddr": network_data["ipaddr"],
                "netmask": network_data["netmask"],
                "gateway": network_data["gateway"],
                "dns_flag": "1",
                "dns1": network_data["dns1"],
                "dns2": network_data["dns2"]}
        else:
            send_data["properties"] = {"proto": network_data["proto"]}
        send_data["topic"] = "/+/+/function_invoke"
        send_data["type"] = "sub"
        send_data = json.dumps(send_data)
        # print(send_data)
        return send_data
    except Exception as e:
        print(traceback.print_exc())

    #################################################################################################

def find_ip(ip_prefix, head, tail, udp_socker, send_data, local_ip):
    """ 循环处理 休眠0.05秒"""
    try:
        send_data = aes_encrypt(send_data)
        for i in range(int(head), int(tail)+1):
            ip = '%s.%s' % (ip_prefix, i)
            if ip == local_ip:
                continue
            udp_socker.sendto(send_data, (ip, 8887))
    except Exception as e:
        pass
        print(traceback.print_exc())


def print_ip_list(com_mand):
    """ 程序 运行 入口 """

    try:
        global udp_recv_dict  # 存放所有消息的字典
        udp_recv_dict = {}

        ip_prefix_list = []     # 存放网关前两个数据
        ip_h_t_list = []        # 存放网关第三个数据
        ip_p_list = []          # 存放网关最后一个数据
        ip_prefix = None

        udp_socker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        localaddr = ('', 9999)
        udp_socker.bind(localaddr)

        for ip_num in com_mand:     # 把起始IP和终止IP进行拆分
            args = "".join(ip_num)  # 无意义 原数据
            ip_prefix = '.'.join(args.split('.')[:-2])  # 取网关前两个数据
            ip_p = '.'.join(args.split('.')[2:-1])  # 取网关第三个数据
            ip_tail = '.'.join(args.split('.')[-1:])    # 取网关最后一个数据
            ip_h_t_list.append(ip_tail)     # 把网关最后一个数据存进列表
            ip_p_list.append(ip_p)      # 把网关第三个数据存进列表


        time_t = int(ip_p_list[1]) - int(ip_p_list[0])  # 网段区间比较

        '''开启接收线程'''
        if time_t > 1:
            _thread.start_new_thread(recv_message, (time_t, udp_socker))
        elif time_t == 0:
            _thread.start_new_thread(recv_message, (1, udp_socker))
        elif time_t == 1:
            _thread.start_new_thread(recv_message, (2, udp_socker))
        else:   # 区间为负则不动作
            udp_socker.close()
            return udp_recv_dict

        for x in range(255):    # 循环合成所有的网段, 并存入ip_prefix_list中
            if int(ip_p_list[0]) == int(ip_p_list[1]):  # 网段区间比较
                ip_prefix_list.append('%s.%s' % (ip_prefix, ip_p_list[0]))
                break
            else:
                ip_prefix_list.append('%s.%s' % (ip_prefix, ip_p_list[0]))
                ip_p_list[0] = int(ip_p_list[0]) + 1


        '''对每个网段下指定的IP都进行基本信息获取'''
        local_ip = get_local_ip()
        for x in ip_prefix_list:
            # x 是网段ip地址 x: 192.168.x
            find_ip(x, ip_h_t_list[0], ip_h_t_list[1], udp_socker, random_sysinfo(), local_ip)   # 传入网段和网段下的IP区间以及套接字

        time.sleep(1)
        udp_socker.close()

        if len(udp_recv_dict) != 0:
            udp_socker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            localaddr = ('', 9999)
            udp_socker.bind(localaddr)
            '''对已经获取到的所有IP地址进行更多信息获取'''
            Acquired_IP_list = list(udp_recv_dict.keys())
            _thread.start_new_thread(recv_message, (len(Acquired_IP_list), udp_socker))
            for mac in Acquired_IP_list:  # 获取子网掩码和http端口
                ip = udp_recv_dict[mac]['ipaddr']
                proto = udp_recv_dict[mac]['proto']
                udp_socker.sendto(aes_encrypt(random_network(mac, proto)), (ip, 8887))
            for mac in Acquired_IP_list:  # 获取服务器指向数据
                ip = udp_recv_dict[mac]['ipaddr']
                send_data = aes_encrypt(random_cloud_config(mac))
                udp_socker.sendto(send_data, (ip, 8887))
            for mac in Acquired_IP_list:  # 获取bdinfo数据
                ip = udp_recv_dict[mac]['ipaddr']
                udp_socker.sendto(aes_encrypt(random_bdinfo(mac)), (ip, 8887))
            time.sleep(1)
            udp_socker.close()

            udp_socker = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            localaddr = ('', 9999)
            udp_socker.bind(localaddr)
            _thread.start_new_thread(recv_message, (len(Acquired_IP_list), udp_socker))
            for mac in Acquired_IP_list:  # 获取频点和频点ID
                ip = udp_recv_dict[mac]['ipaddr']
                bdinfo_mode = udp_recv_dict[mac]['bdinfo']
                udp_socker.sendto(aes_encrypt(random_module_config(mac, bdinfo_mode)), (ip, 8887))
            time.sleep(1)
            udp_socker.close()

            device_tpye_divide()    # 进行设备类型区分
        if udp_recv_dict:
            return udp_recv_dict
        else:
            return None
    except Exception as e:
        print(traceback.print_exc())
        return ''


def exec_command(comands):#指定返回类型为list类型
    """执行windows命令"""
    try:
        if comands == None:
            return
        #创建子进程执行指令，使用shell解释器,指定输出到标准输出，所有的换行用\n代替
        p = subprocess.Popen(comands, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        result = "".join(p.stdout.readlines())#获取返回结果并拼接数据
        return result
    except Exception as e:
        print(traceback.print_exc())

def get_net_card():#指定返回类型为list类型
    """获取本机的网络ip"""
    try:
        ip_list_2 = []#IP列表
        net_card_data = []#用来存放网卡数据
        temp_dict = dict(flag=True)
        gateway_error = False
        result = exec_command('ipconfig')
        # 在输出结果里是否保留换行符('\r', '\r\n', \n')，默认为 False，不包含换行符，如果为 True，则保留换行符
        result = result.splitlines()
        # 匹配IP正则
        pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        for data in result:
            # print(data,type(data),len(data))
            if gateway_error:
                temp_dict['gateway1'] = pattern.search(data)
                gateway_error = False
                # print("当前网卡 %s 获取第二行网关信息 %s" % (temp_dict['card_name'], temp_dict['gateway1']))
                continue
            # 如果发现新的适配器，则重置上一个网卡是否可用的状态
            if "适配器" in data:
                temp_dict = dict(flag=True)
                temp_dict['card_name'] = data.split(" ", 1)[1][:-1]
                # print("当前网卡 %s" % (temp_dict['card_name']))
                continue
            if "IPv4 地址" in data:
                temp_dict['ip'] = pattern.search(data).group()
                # print("当前网卡 %s 获取IP信息 %s" % (temp_dict['card_name'], temp_dict['ip']))
                continue
            elif "子网掩码" in data:
                temp_dict['mask'] = pattern.search(data).group()
                # print("当前网卡 %s 获取子网掩码信息 %s" % (temp_dict['card_name'], temp_dict['mask']))
                continue
            # 测试发现有的网关会默认在下一行，情况见说明一，所以这边做了异常处理
            elif "默认网关" in data:
                try:
                    temp_dict['gateway1'] = pattern.search(data).group()
                    # print("当前网卡 %s 获取默认网关信息 %s" % (temp_dict['card_name'], temp_dict['gateway1']))
                    ip_list_2.append(temp_dict['gateway1'])
                except:
                    gateway_error = True
                    # print("当前网卡 %s 解析当前行默认网关信息错误" % (temp_dict['card_name']))
                # 如果检查到网关，代表当前适配器信息已经获取完毕 重置网关状态与适配器信息字典
                if temp_dict.get("gateway1"):
                    net_card_data.append(temp_dict)
                    # print("当前网卡 %s 当前适配器信息获取完毕 %s \n\n" % (temp_dict['card_name'], temp_dict))
                    temp_dict = dict(flag=True)
                    continue
            # 发现媒体已断开则更改当前适配器状态
            elif "媒体已断开" in data:
                # print("当前网卡 %s 已断开 跳过\n\n" % (temp_dict['card_name']))
                temp_dict['flag'] = False
                continue
            # 判断媒体状态正常，IP、子网掩码、网关都正常后，保持起来
            if temp_dict.get("flag") and temp_dict.get("ip") and temp_dict.get("mask") and temp_dict.get(
                    "gateway1"):
                # print("当前网卡 %s 当前适配器信息获取完毕 %s \n\n" % (temp_dict['card_name'], temp_dict))
                net_card_data.append(temp_dict)
                # 重置网关状态与适配器信息字典
                temp_dict = dict(flag=True)
                continue
        return ip_list_2
    except Exception as e:
        print(traceback.print_exc())


    #############################################数据加解密###########################################
def get_Invisible_key():
    '''生成不可见密钥'''
    data = ""
    while len(data) < 16:
        data += chr(random.randint(11, 31))
    return data

def deviation_data(data, n, mode=1):
    '''密钥偏移数据'''
    try:
        if type(n) != int:
            return
        result = ""
        if mode == 1:
            for i in range(len(data)):
                result += chr(ord(data[i:i + 1]) + n)
        elif mode == 2:
            for i in range(len(data)):
                result += chr(ord(data[i:i + 1]) - n)
        return result
    except Exception as e:
        print(traceback.print_exc())

def iv_Encryption_decryption(data, n, mode = 1):
    '''iv加密与解密， 采用奇正偶负偏移加密法'''
    try:
        if type(n) != int:
            return
        result = ""
        if mode == 1:   #iv加密
            for i in range(len(data)):
                if i % 2 == 0:
                    result += chr(ord(data[i:i + 1]) + n)
                else:
                    result += chr(ord(data[i:i + 1]) - n)
        elif mode == 2: #iv解密
            for i in range(len(data)):
                if i % 2 == 0:
                    result += chr(ord(data[i:i + 1]) - n)
                else:
                    result += chr(ord(data[i:i + 1]) + n)
        return result
    except Exception as e:
        print(traceback.print_exc())


def pkcs7padding(text):
    """
    明文使用PKCS7填充
    """
    try:
        bs = 16  # 密钥长度
        length = len(text)  # 数据长度
        bytes_length = len(text.encode('utf-8'))  # 转换以后的数据长度
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs  # 计算要填充的数字
        padding_text = chr(padding) * padding  # 生成要填充的数据

        return text + padding_text  # 填充数据接在原数据后面
    except Exception as e:
        print(traceback.print_exc())

def aes_encrypt(content):
    """
    AES加密
    """
    try:
        add_num = random.randint(1, 10)
        key = get_Invisible_key().encode("utf-8")  #获取不可见密钥
        key_deviation = deviation_data(key.decode("utf-8"), add_num)
        iv = deviation_data(key.decode("utf-8"), add_num, 2).encode("utf-8")

        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 处理明文
        content_padding = pkcs7padding(content)
        # print(content_padding, len(content_padding))
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # print(encrypt_bytes, len(encrypt_bytes))
        # 进行拼接
        send_data = key_deviation.encode('utf-8') + (chr(add_num)).encode('utf-8') + encrypt_bytes
        # 重新编码
        # send_data = str(base64.b64encode(send_data), encoding='utf-8')
        # send_data = str(send_data, encoding='utf-8')
        # print(send_data, len(send_data))
        return send_data
    except Exception as e:
        print(traceback.print_exc())


def aes_decrypt(content):
    """
    AES解密
    """
    try:
        # content = base64.b64decode(content)  # base64解码
        # print('error', content, type(content))
        key = (content[0:16])  # 获取密钥
        add_num = (content[16:17])  # 获取偏移量
        data = content[17:]  # 获取数据

        key = deviation_data(key.decode("utf-8"), ord(add_num), 2).encode("utf-8")
        iv = deviation_data(key.decode("utf-8"), ord(add_num.decode("utf-8")), 2).encode("utf-8")

        cipher = AES.new(key, AES.MODE_CBC, iv)     # aes解密
        text = cipher.decrypt(data).decode('utf-8')
        text = pkcs7padding(text)   # 明文填充
        for i in range(32):     # 去除不可见字符
            text = text.replace(chr(i), '')
        text = json.loads(text)     #解除json
        return text

    except Exception as e:

        print(traceback.print_exc())

    #############################################http模块###########################################
def bulid_http_server():
    '''搭建http服务器'''
    try:
        port = 8888
        httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
        httpd.serve_forever()
    except Exception as e:
        print(traceback.print_exc())

def get_local_ip():
    '''获取当前使用的IP'''
    try:
        interface_data = psutil.net_if_stats()
        interface_address_information = psutil.net_if_addrs()
        # print(interface_address_information)
        key_list = list(interface_data.keys())
        for key in key_list:
            if '以太网' in key or 'WLAN' in key or 'Ethernet' in key:
                if interface_data[key].isup == True:
                    addr_info_list = interface_address_information[key]
                    for addr_info in addr_info_list:
                        if addr_info.family == 2:
                            return addr_info.address
        return None
    except Exception as e:
        print(traceback.print_exc())

def copy_file(source, target):
    '''复制文件'''
    try:
        filename = source.split('/')[-1:][0]
        if os.path.exists('./bdinfo/%s' % filename) == True:
            return './bdinfo/%s' % filename
        result = shutil.copy(source, target)
        return result
    except Exception as e:
        print(traceback.print_exc())
        return False

    ###########################################时间模块######################################
def _format_offset(seconds_offset):
    """
    将偏移秒数转换为UTC±X
    注意：这里没有考虑时区偏移非整小时的，使用请修改处理方式
    :param seconds_offset 偏移秒数
    :return: 格式化后的时区偏移
    """
    hours_offset = float(seconds_offset / 60 / 60)
    if hours_offset >= 0:
        return "UTC+" + str(hours_offset)
    else:
        return "UTC" + str(hours_offset)

def time_zone_offset(timedata):
    '''时区偏移'''
    try:
        seconds_offset = time.localtime().tm_gmtoff
        date_utc = _format_offset(seconds_offset)
        offset = float(date_utc.replace('UTC', ''))
        all_offset_min = 60 * offset

        time_list = timedata.split(':')
        hour = int(time_list[0])
        min = int(time_list[1])
        settime = hour * 60 + min
        settime -= all_offset_min
        if settime > 1440:
            settime -= 1440
        elif settime < 0:
            settime += 1440
        min = settime % 60
        hour = (settime - min) / 60


        return str(hour), str(min)

    except Exception as e:
        print(traceback.print_exc())

if __name__ == '__main__':
    data = aes_encrypt('''{"service": "webox","resource": "wifi","cmd": "get","para": "","serial": 12345}''')
    data_2 = aes_decrypt(data)
    print(type(data_2), data_2)